import os
import random
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

import speech_recognition as sr
import pyttsx3
from google import genai

# ROBO - a laptop-only AI exhibition assistant
# Install packages:
# python -m pip install google-genai SpeechRecognition pyttsx3 pyaudio

BG = "#101827"
PANEL = "#192538"
CYAN = "#42e8f5"
WHITE = "#f4f7fb"
MUTED = "#aabbd0"

QUIZ = [
    ("Which planet is known as the Red Planet?", ["Mars", "Venus", "Jupiter"], "Mars"),
    ("What does AI stand for?", ["Automatic Internet", "Artificial Intelligence", "Advanced Input"], "Artificial Intelligence"),
    ("Which animal is the largest mammal?", ["Elephant", "Blue whale", "Giraffe"], "Blue whale"),
    ("How many sides does a hexagon have?", ["Five", "Six", "Eight"], "Six"),
]

class RoboApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ROBO - Your AI Friend")
        self.root.geometry("850x760")
        self.root.minsize(700, 650)
        self.root.configure(bg=BG)

        self.client = None
        self.chat = None
        self.busy = False
        self.quiz_index = 0
        self.quiz_score = 0
        self.quiz_active = False
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8

        try:
            self.voice = pyttsx3.init()
            self.voice.setProperty("rate", 165)
            self.voice.setProperty("volume", 1.0)
        except Exception:
            self.voice = None

        header = tk.Label(root, text="🤖  ROBO — YOUR AI FRIEND", font=("Arial", 23, "bold"),
                          bg=BG, fg=CYAN)
        header.pack(pady=(14, 4))
        tk.Label(root, text="Talk • Ask • Laugh • Learn", font=("Arial", 11),
                 bg=BG, fg=MUTED).pack(pady=(0, 8))

        # Animated robot face
        self.face = tk.Canvas(root, width=300, height=170, bg=BG, highlightthickness=0)
        self.face.pack()
        self.draw_face()
        self.root.after(500, self.blink)

        # API key entry; key is kept in memory and is not written to the file.
        key_frame = tk.Frame(root, bg=BG)
        key_frame.pack(fill="x", padx=20, pady=(2, 8))
        tk.Label(key_frame, text="Gemini API key:", bg=BG, fg=WHITE,
                 font=("Arial", 10, "bold")).pack(side="left")
        self.key_entry = tk.Entry(key_frame, show="*", width=38, font=("Arial", 10),
                                  bg=PANEL, fg=WHITE, insertbackground=WHITE,
                                  relief="flat")
        self.key_entry.pack(side="left", padx=8, ipady=5)
        self.key_entry.insert(0, os.getenv("GEMINI_API_KEY", ""))
        tk.Button(key_frame, text="Connect AI", command=self.connect_ai,
                  bg="#176b78", fg=WHITE, relief="flat", padx=10).pack(side="left")

        self.status = tk.Label(root, text="Ready! Connect AI, then type or talk to me.",
                               font=("Arial", 10), bg=BG, fg=CYAN)
        self.status.pack(pady=(0, 6))

        self.chatbox = scrolledtext.ScrolledText(
            root, height=12, wrap=tk.WORD, font=("Arial", 11),
            bg=PANEL, fg=WHITE, insertbackground=WHITE,
            relief="flat", padx=10, pady=8
        )
        self.chatbox.pack(fill="both", expand=True, padx=20, pady=5)
        self.chatbox.insert(tk.END,
            "ROBO: Hello, human! 👋 I'm your AI exhibition buddy.\n"
            "Try asking me a question, asking for a joke, or starting a quiz.\n\n")
        self.chatbox.configure(state="disabled")

        input_frame = tk.Frame(root, bg=BG)
        input_frame.pack(fill="x", padx=20, pady=(8, 4))
        self.message_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#ffffff",
                                      fg="#111827", relief="flat")
        self.message_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self.message_entry.bind("<Return>", lambda event: self.send_text())
        tk.Button(input_frame, text="Send ➤", command=self.send_text, bg=CYAN,
                  fg=BG, font=("Arial", 10, "bold"), relief="flat", padx=15).pack(side="left")

        button_frame = tk.Frame(root, bg=BG)
        button_frame.pack(pady=(5, 14))
        self.talk_button = tk.Button(button_frame, text="🎤 TALK TO ROBO",
            command=self.listen, bg="#087f8c", fg=WHITE, font=("Arial", 11, "bold"),
            relief="flat", padx=14, pady=9)
        self.talk_button.pack(side="left", padx=5)
        tk.Button(button_frame, text="😂 Tell a joke", command=self.joke,
            bg="#6d4cc3", fg=WHITE, font=("Arial", 10, "bold"),
            relief="flat", padx=12, pady=9).pack(side="left", padx=5)
        tk.Button(button_frame, text="🎮 Start quiz", command=self.start_quiz,
            bg="#247a49", fg=WHITE, font=("Arial", 10, "bold"),
            relief="flat", padx=12, pady=9).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear chat", command=self.clear_chat,
            bg="#38465b", fg=WHITE, font=("Arial", 10),
            relief="flat", padx=12, pady=9).pack(side="left", padx=5)

    def draw_face(self, blink=False, speaking=False):
        self.face.delete("all")
        # Robot head
        self.face.create_oval(45, 8, 255, 160, fill="#1b3448", outline=CYAN, width=3)
        self.face.create_arc(105, 0, 195, 45, start=0, extent=180, style="arc",
                             outline=CYAN, width=3)
        self.face.create_line(150, 4, 150, 0, fill=CYAN, width=3)
        self.face.create_oval(143, 0, 157, 10, fill="#ffcb6b", outline="")
        # Eyes
        if blink:
            self.face.create_line(82, 67, 122, 67, fill=CYAN, width=5)
            self.face.create_line(178, 67, 218, 67, fill=CYAN, width=5)
        else:
            self.face.create_oval(82, 45, 124, 88, fill=CYAN, outline="")
            self.face.create_oval(178, 45, 220, 88, fill=CYAN, outline="")
            self.face.create_oval(96, 56, 109, 72, fill="#102033", outline="")
            self.face.create_oval(192, 56, 205, 72, fill="#102033", outline="")
        # Cheeks and mouth
        self.face.create_oval(66, 91, 91, 104, fill="#ee7c91", outline="")
        self.face.create_oval(209, 91, 234, 104, fill="#ee7c91", outline="")
        if speaking:
            self.face.create_oval(123, 99, 177, 131, fill="#07111d", outline=CYAN, width=2)
        else:
            self.face.create_arc(118, 91, 182, 137, start=200, extent=140,
                                 style="arc", outline=CYAN, width=4)

    def blink(self):
        if not self.root.winfo_exists():
            return
        self.draw_face(blink=True)
        self.root.after(180, self.draw_face)
        self.root.after(random.randint(1800, 3500), self.blink)

    def add_line(self, text):
        self.chatbox.configure(state="normal")
        self.chatbox.insert(tk.END, text + "\n\n")
        self.chatbox.see(tk.END)
        self.chatbox.configure(state="disabled")

    def connect_ai(self):
        key = self.key_entry.get().strip()
        if not key or key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
            messagebox.showinfo("API key needed",
                "Create a Gemini API key in Google AI Studio, then paste it in the API key box.")
            return
        try:
            self.client = genai.Client(api_key=key)
            self.chat = self.client.chats.create(model="gemini-2.5-flash")
            self.status.config(text="AI connected! Type a message or press TALK TO ROBO.")
            self.add_line("ROBO: My AI brain is connected. Let's talk!")
        except Exception as e:
            self.status.config(text="Could not connect. Check the key and internet.")
            messagebox.showerror("Connection error", str(e)[:500])

    def set_busy(self, value, status_text=None):
        self.busy = value
        self.talk_button.config(state="disabled" if value else "normal")
        if status_text:
            self.status.config(text=status_text)

    def send_text(self):
        text = self.message_entry.get().strip()
        if not text or self.busy:
            return
        self.message_entry.delete(0, tk.END)
        if self.quiz_active:
            self.add_line("YOU: " + text)
            self.check_quiz_answer(text)
        else:
            self.ask_ai(text)

    def ask_ai(self, question):
        if self.client is None or self.chat is None:
            messagebox.showinfo("Connect the AI first",
                "Paste your Gemini API key in the box and press Connect AI.")
            return
        self.set_busy(True, "🧠 ROBO is thinking...")
        self.add_line("YOU: " + question)
        threading.Thread(target=self.ai_worker, args=(question,), daemon=True).start()

    def ai_worker(self, question):
        try:
            prompt = (
                "You are ROBO, a friendly, funny AI robot at a college exhibition "
                "for teenagers. Answer simply and helpfully in 2-5 sentences. "
                "Tell clean jokes if asked. If asked for a quiz, ask one short "
                "question and wait for the visitor's answer. Do not claim to know "
                "private information. Visitor says: " + question
            )
            response = self.chat.send_message(message=prompt)
            answer = response.text or "Oops! I couldn't form an answer."
            self.root.after(0, lambda a=answer: self.ai_done(a))
        except Exception as e:
            msg = str(e)[:250]
            self.root.after(0, lambda m=msg: self.ai_error(m))

    def ai_done(self, answer):
        self.add_line("ROBO: " + answer)
        self.set_busy(False, "✨ Your turn! Ask me something else.")
        self.speak(answer)

    def ai_error(self, message):
        self.set_busy(False, "AI request failed. Check internet, API key, and quota.")
        self.add_line("ROBO: Sorry, I couldn't reach my AI service.")
        messagebox.showerror("AI error", message)

    def listen(self):
        if self.busy:
            return
        self.set_busy(True, "🎤 Listening... speak after this message.")
        threading.Thread(target=self.listen_worker, daemon=True).start()

    def listen_worker(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=12)
            words = self.recognizer.recognize_google(audio)
            self.root.after(0, lambda w=words: self.voice_received(w))
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.listen_error("I didn't hear anything. Press the mic and try again."))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.listen_error("I couldn't understand. Please speak clearly."))
        except sr.RequestError:
            self.root.after(0, lambda: self.listen_error("Speech service unavailable. Check your internet."))
        except Exception as e:
            msg = str(e)[:200]
            self.root.after(0, lambda m=msg: self.listen_error("Microphone problem: " + m))

    def voice_received(self, words):
        self.set_busy(False, "🧠 I heard you! Thinking...")
        if self.quiz_active:
            self.add_line("YOU: " + words)
            self.check_quiz_answer(words)
        else:
            self.ask_ai(words)

    def listen_error(self, message):
        self.set_busy(False, message)

    def speak(self, text):
        if self.voice is None:
            self.status.config(text="Text answer ready; text-to-speech is unavailable.")
            return
        def worker():
            try:
                self.root.after(0, lambda: self.draw_face(speaking=True))
                self.voice.say(text)
                self.voice.runAndWait()
            except Exception:
                pass
            finally:
                self.root.after(0, self.draw_face)
        threading.Thread(target=worker, daemon=True).start()

    def joke(self):
        jokes = [
            "Why did the computer go to the doctor? It caught a virus!",
            "Why was the robot tired? It had a hard drive!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "What is a robot's favourite snack? Computer chips!"
        ]
        joke = random.choice(jokes)
        self.quiz_active = False
        self.add_line("ROBO: " + joke)
        self.speak(joke)
        self.status.config(text="😂 Joke time! Try another button.")

    def start_quiz(self):
        self.quiz_active = True
        self.quiz_index = 0
        self.quiz_score = 0
        self.show_quiz_question()

    def show_quiz_question(self):
        if self.quiz_index >= len(QUIZ):
            result = f"Quiz finished! You scored {self.quiz_score} out of {len(QUIZ)}. Great job!"
            self.add_line("ROBO: " + result)
            self.speak(result)
            self.quiz_active = False
            self.status.config(text="Quiz complete! Start again to replay.")
            return
        question, options, _ = QUIZ[self.quiz_index]
        prompt = f"Question {self.quiz_index + 1}: {question} Options: " + ", ".join(options)
        self.add_line("ROBO: " + prompt + "\nSay your answer, or type it below.")
        self.speak(prompt)
        self.status.config(text="Quiz mode: answer by typing or using the microphone.")

    def check_quiz_answer(self, answer):
        correct = QUIZ[self.quiz_index][2]
        if correct.lower() in answer.lower():
            self.quiz_score += 1
            reply = "Correct! Nice one."
        else:
            reply = "Good try! The correct answer is " + correct + "."
        self.add_line("ROBO: " + reply)
        self.speak(reply)
        self.quiz_index += 1
        self.root.after(1200, self.show_quiz_question)

    def clear_chat(self):
        self.chatbox.configure(state="normal")
        self.chatbox.delete("1.0", tk.END)
        self.chatbox.configure(state="disabled")
        self.add_line("ROBO: Chat cleared. I'm ready!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoboApp(root)
    root.mainloop()
