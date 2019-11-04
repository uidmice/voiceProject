from piwho import recognition
recog =recognition.SpeakerRecognizer()
name =[]
name = recog.identify_speaker('/home/pi/Projects/voiceProject/models/testing/reese.wav')
print(name[0])
print(name[1])
#dictn = recog.get_speaker_scores()
#print dictn