
import speech_recognition as sr

recognizer = sr.Recognizer()

print("Checking microphone...")

try:
    with sr.Microphone() as source:
        print("Microphone detected!")
        print("Say something...")

        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)

    print("Recognizing your voice...")

    text = recognizer.recognize_google(audio)
    print("You said:", text)

except Exception as e:
    print("Error:", e)
