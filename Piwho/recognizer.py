from piwho import recognition
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("recording", help="file for speaker recognition")
args = parser.parse_args()

test_path_dir = "/home/pi/voiceProject/"
recog =recognition.SpeakerRecognizer()
name =[]
file = '{0}{1}'.format(test_path_dir,args.recording)
print file
name = recog.identify_speaker(file)
print name[0]
