#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import struct
import sys
from datetime import datetime
from threading import Thread
from threading import Timer
from multiprocessing import Process


import numpy as np
import pyaudio
import soundfile

from porcupine import Porcupine

WAKE_WORD = "hey pico"
CMD1 = "terminator"
CMD2 = "blueberry"
CMD3 = "picovoice"
LIBRARY_PATH = "porcupine/lib/raspberry-pi/cortex-a53/libpv_porcupine.so"
MODEL_FILE_PATH = "porcupine/lib/common/porcupine_params.pv"
INPUT_DEVICE_INDEX = 5

S1 ="porcupine/resources/keyword_files/raspberrypi/" + WAKE_WORD + "_raspberrypi.ppn"
S2 ="porcupine/resources/keyword_files/raspberrypi/" + CMD1 + "_raspberrypi.ppn"
S3 ="porcupine/resources/keyword_files/raspberrypi/" + CMD2 + "_raspberrypi.ppn"
S4 ="porcupine/resources/keyword_files/raspberrypi/" + CMD3 + "_raspberrypi.ppn"

KEYWORD_FILE_PATHS = [S1, S2, S3, S4]
SENSITIVITIES = [1.0, 1.0, 1.0, 1.0]
OUTPUT_PATH = "./temp.wav"

status = 0 # 0: idle, 1: keyword detected, 2: CMD1 detected, 3: CMD2 detected, 4: CMD3 detected


def timer_callback():
    global status
    status = 0

def cmd1():
    print("CMD1: %s" %CMD1)

def cmd2():
    print("CMD2: %s" %CMD2)

def cmd3():
    print("CMD3: %s" %CMD3)

def storeFile(frames, i, sample_rate):
    recorded_audio = np.concatenate(frames, axis=0).astype(np.int16)
    filename = "./tem" + str(i) + ".wav"
    print (len(recorded_audio))
    soundfile.write(filename, recorded_audio[-sample_rate*2:][:], samplerate=sample_rate, subtype='PCM_16')

class MyPorcupine(Thread):

    def __init__(
            self,
            library_path=LIBRARY_PATH,
            model_file_path=MODEL_FILE_PATH,
            keyword_file_paths=KEYWORD_FILE_PATHS,
            sensitivities=SENSITIVITIES,
            input_device_index=INPUT_DEVICE_INDEX,
            output_path=OUTPUT_PATH):

        super(MyPorcupine, self).__init__()

        self._library_path = library_path
        self._model_file_path = model_file_path
        self._keyword_file_paths = keyword_file_paths
        self._sensitivities = sensitivities
        self._input_device_index = input_device_index
        self._output_path = output_path
        self._recorded_frames = []

    def run(self):
        global status
        num_keywords = len(self._keyword_file_paths)

        keyword_names = list()
        for x in self._keyword_file_paths:
            keyword_names.append(os.path.basename(x).replace('.ppn', '').replace('_compressed', '').split('_')[0])

        print('listening for:')
        for keyword_name, sensitivity in zip(keyword_names, self._sensitivities):
            print('- %s (sensitivity: %f)' % (keyword_name, sensitivity))

        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = Porcupine(
                library_path=self._library_path,
                model_file_path=self._model_file_path,
                keyword_file_paths=self._keyword_file_paths,
                sensitivities=self._sensitivities)
            print("sample rate: "+ str(porcupine.sample_rate) + "\n")
            print("frame length: "+ str(porcupine.frame_length) + "\n")
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length,
                input_device_index=self._input_device_index)
            i = 0

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                if self._output_path is not None and status == 0:
                    self._recorded_frames.append(pcm)

                result = porcupine.process(pcm)

                if status ==0:
                    if result == 0: #wake word detected
                        print('detected %s' % ( keyword_names[result]))
                        status = 1
                        timer = Timer(10.0, timer_callback)
                        timer.start()
                        if self._output_path is not None and len(self._recorded_frames) > 0:
                            i += 1
                            storeProcess = Process(target=storeFile, args=(self._recorded_frames, i, porcupine.sample_rate))
                            storeProcess.start()
                            self._recorded_frames = []
                        continue

                if status == 1:
                    if result > 0:
                        print('detected %s' % ( keyword_names[result]))
                        status = result + 1

                if status == 2:
                    timer.cancel()
                    cmd1()
                    status = 0


                if status == 3:
                    timer.cancel()
                    cmd2()
                    status = 0

                if status == 4:
                    timer.cancel()
                    cmd3()
                    status = 0




        except KeyboardInterrupt:
            print('stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()

            if self._output_path is not None and len(self._recorded_frames) > 0:
                recorded_audio = np.concatenate(self._recorded_frames, axis=0).astype(np.int16)
                soundfile.write(self._output_path, recorded_audio, samplerate=porcupine.sample_rate, subtype='PCM_16')

    _AUDIO_DEVICE_INFO_KEYS = ['index', 'name', 'defaultSampleRate', 'maxInputChannels']

    @classmethod
    def show_audio_devices_info(cls):
        """ Provides information regarding different audio devices available. """

        pa = pyaudio.PyAudio()

        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print(', '.join("'%s': '%s'" % (k, str(info[k])) for k in cls._AUDIO_DEVICE_INFO_KEYS))

        pa.terminate()

def main():
    MyPorcupine.show_audio_devices_info()
    MyPorcupine().run()

if __name__=="__main__":
    main()
