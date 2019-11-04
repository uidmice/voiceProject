from piwho import recognition

recog = recognition.SpeakerRecognizer("/home/pi/Projects/voiceProject/models/eve")
recog.speaker_name ='Eve'
recog.train_new_data()

recog = recognition.SpeakerRecognizer('/home/pi/Projects/voiceProject/models/akansha')
recog.speaker_name ='Akansha'
recog.train_new_data()

recog = recognition.SpeakerRecognizer('/home/pi/Projects/voiceProject/models/JAWAHAR')
recog.speaker_name ='Jawahar'
recog.train_new_data()

print recog.get_speakers()
