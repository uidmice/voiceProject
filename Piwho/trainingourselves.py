from piwho import recognition
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("name", help="the name for the training model")
parser.add_argument("-f", help="(optional) specific file for training")
args = parser.parse_args()

model_path_dir = '/home/pi/Projects/voiceProject/models/'

def train_speaker(name, *args):
    recog = recognition.SpeakerRecognizer('{0}{1}'.format(model_path_dir,name))
    recog.speaker_name = name
    if(len(args)==1):
        recog.train_new_data(args[0])

train_speaker(args.name)

print recog.get_speakers()
