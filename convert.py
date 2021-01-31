import speech_recognition as sr
import time 


class AshleyContext:
    exit_app = False

def recognize_audio(recognizer, audio):
    try:
        print("Start recognition")
        recognized_audio = recognizer.recognize_google(audio) 
        print("You have said : \n " + recognized_audio)
        if recognized_audio == "Ashley stop":
            
            AshleyContext.exit_app = True

    except sr.UnknownValueError:
        print("Sorry I didn't understant that!")

def main():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

    print("Please say something...")
    audio = r.listen_in_background(source, recognize_audio)
    
    while True:
        time.sleep(1)
        if AshleyContext.exit_app:
            audio()
            print("Thank you for using ashley.")
            break
        
       
if __name__ == "__main__":
    main()