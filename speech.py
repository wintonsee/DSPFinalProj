# Before you start, install Speech Recognition library by following command:
# Mac: sudo pip3 install SpeechRecognition
# Windows: pip install SpeechRecognition

import speech_recognition as sr

r = sr.Recognizer()

#with sr.WavFile("demo_07_Exer4.wav") as source:
with sr.Microphone() as source:
    print('Speak something')
    audio = r.listen(source, timeout = None)

    try: 
        text = r.recognize_google(audio)
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize your voice")
