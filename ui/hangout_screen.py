# for vibe quiz & spot suggestions
import tkinter as tk
from random import sample
from ui.memory_screen import MemoryScreen

class HangoutScreen:
    def __init__(self, state):
        self.state = state
        self.root = state.root
        self.current_question = 0
        self.answers = []

        self.questions = [
            ("What's your mood today?", ["😌 Chill", "🎉 Fun", "🧠 Intellectual", "🏄 Adventure"]),
            ("Who's coming with you?", ["Just me/+1", "Small group", "Big group"]),
            ("What's your budget?", ["💰 < AED 50", "💵 50-150", "💸 > AED 150"])
        ]

    def show(self):
        self.clear()
        self.show_question()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_question(self):
        self.clear()
        bg = self.state.colors["background"]
        text = self.state.colors["text"]
        accent = self.state.colors["accent"]

        if self.current_question >= len(self.questions):
            self.show_results()
            return

        q, options = self.questions[self.current_question]
        tk.Label(self.root, text=q, font=("Courier", 16, "bold"), bg=bg, fg=text).pack(pady=30)
        frame = tk.Frame(self.root, bg=bg)
        frame.pack()

        for opt in options:
            tk.Button(frame, text=opt, font=("Courier", 12), bg=accent, fg=text, width=25, pady=10, command=lambda o=opt: self.record_answer(o)).pack(pady=5)

    def record_answer(self, answer):
        self.answers.append(answer)
        self.current_question += 1
        self.show_question()

    def show_results(self):
        self.clear()
        bg = self.state.colors["background"]
        text = self.state.colors["text"]

        tk.Label(self.root, text="Your Matches", font=("Courier", 20, "bold"), bg=bg, fg=text).pack(pady=20)
        tk.Label(self.root, text="Top hangout spots for you:", font=("Courier", 12), bg=bg, fg=text).pack(pady=10)

        frame = tk.Frame(self.root, bg=bg)
        frame.pack(pady=20)

        matches = sample(self.state.stamps, min(3, len(self.state.stamps)))
        for stamp in matches:
            s = f"{stamp['title']} — {stamp['location']} ({stamp['budget']})"
            tk.Button(frame, text=s, font=("Courier", 10), bg=self.state.colors["secondary"], fg="white", command=lambda s=stamp: self.select_stamp(s)).pack(pady=5)

    def select_stamp(self, stamp):
        self.state.current_stamp = stamp
        self.state.show_screen(MemoryScreen)
