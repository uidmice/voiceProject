from piwho import recognition
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("recording", help="file for speaker recognition")
args = parser.parse_args()

test_path_dir = "/home/pi/Projects/voiceProject/models/testing/"
recog =recognition.SpeakerRecognizer()
name =[]
name = recog.identify_speaker('{0}{1}'.format(test_path_dir,args.recording))
print(name[0])
print(name[1])
dictn = recog.get_speaker_scores()
print dictn