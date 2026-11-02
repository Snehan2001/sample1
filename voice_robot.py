
import speech_recognition as sr
import pyttsx3
import datetime
import pyjokes
import webbrowser

robot = pyttsx3.init()
robot.setProperty("rate", 160)

def speak(text):
    print("ROBOT:", text)
    robot.say(text)
    robot.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        speak("I am listening. Please speak.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("YOU:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand.")
        return ""

    except sr.RequestError:
        speak("Please check your internet connection.")
        return ""

speak("Hello! I am Robo. You can talk to me.")

while True:

    command = listen()

    if "hello" in command or "hi" in command:
        speak("Hello! Welcome to my exhibition.")

    elif "your name" in command:
        speak("My name is Robo.")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + time)

    elif "joke" in command:
        speak(pyjokes.get_joke())

    elif "youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "google" in command:
        speak("Opening Google.")
        webbrowser.open("https://google.com")

    elif "how are you" in command:
        speak("I am doing great. Thank you!")

    elif "bye" in command or "stop" in command:
        speak("Goodbye! See you again.")
        break

    elif command:
        speak("I am still learning. Please ask me something else.")
