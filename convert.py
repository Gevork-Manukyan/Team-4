import speech_recognition as sr
import time 


class SpeechEngine:
    
    def __init__(self):
        self.amIListening = False
        self.r = sr.Recognizer()
        self.cancelListen = None

    def start(self, callBack):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)

        def recognize_audio(recognizer, audio):
            try:
                recognized_audio = recognizer.recognize_google(audio) 
                callBack(recognized_audio)
               
            except sr.UnknownValueError:
                print("Sorry I didn't understant that!")

        self.cancelListen = self.r.listen_in_background(source, recognize_audio)
        print("Start recognition")

    def stop(self):
        self.cancelListen()


def main():
    
    Engine = SpeechEngine()
    Engine.start(print)
    time.sleep(50)
    Engine.stop()
        
       
if __name__ == "__main__":
    main()