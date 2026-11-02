
import pyttsx3
import datetime
import pyjokes
import webbrowser

# Initialize robot voice
engine = pyttsx3.init()
engine.setProperty("rate", 160)

def speak(text):
    print("ROBOT:", text)
    engine.say(text)
    engine.runAndWait()

# Robot introduction
speak("Hello! I am your AI robot.")
speak("Welcome to my world. How can I help you?")

# Main conversation
while True:

    command = input("\nYou: ").lower()

    if "hello" in command or "hi" in command:
        speak("Hello! Nice to meet you.")

    elif "your name" in command:
        speak("My name is Robo. I am your virtual assistant.")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    elif "joke" in command:
        speak(pyjokes.get_joke())

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "how are you" in command:
        speak("I am doing great. Thank you for asking!")

    elif "bye" in command or "exit" in command:
        speak("Goodbye! Have a wonderful day.")
        break

    else:
        speak("Sorry, I don't understand that command yet.")
