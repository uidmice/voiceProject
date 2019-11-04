from piwho import recognition
from piwho import vad
def find_speaker():
    recog = recognition.SpeakerRecognizer()
    
    #recording the voice
    #saving the recording
    vad.record
    
    #using the newly recorded file to test
    
    name = []
    name = recog.identify_speaker()
    return name
#if _name_=='_main_':

speaker= find_speaker()
print ("the closet match")
print(speaker[0])
    