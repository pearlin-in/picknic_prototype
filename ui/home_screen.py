# for showing greeting, options
import tkinter as tk
from ui.hangout_screen import HangoutScreen
from ui.memory_screen import MemoryScreen
from ui.profile_screen import ProfileScreen

class HomeScreen:
    def __init__(self, state):
        self.state = state
        self.root = state.root

    def show(self):
        self.clear()
        bg = self.state.colors["background"]
        text = self.state.colors["text"]
        accent = self.state.colors["accent"]
        secondary = self.state.colors["secondary"]

        # Welcome Message
        tk.Label(self.root, text=f"Welcome back, {self.state.current_user}!",
                 font=("Courier", 20, "bold"), bg=bg, fg=text).pack(pady=30)

        tk.Label(self.root, text="What would you like to do today?",
                 font=("Courier", 12), bg=bg, fg=text).pack(pady=10)

        # Option Buttons
        frame = tk.Frame(self.root, bg=bg)
        frame.pack(pady=30)

        tk.Button(
            frame,
            text="🎯 Find a Hangout Spot",
            font=("Courier", 14, "bold"),
            bg=accent,
            fg=text,
            padx=30,
            pady=15,
            command=lambda: self.state.show_screen(HangoutScreen)
        ).grid(row=0, column=0, padx=20, pady=10)

        tk.Button(
            frame,
            text="✉️ Check Your Mail",
            font=("Courier", 14, "bold"),
            bg=secondary,
            fg=text,
            padx=30,
            pady=15,
            command=lambda: self.state.show_screen(MemoryScreen)
        ).grid(row=0, column=1, padx=20, pady=10)

        tk.Button(
            frame,
            text="👤 Profile",
            font=("Courier", 14, "bold"),
            bg=accent,
            fg=text,
            padx=30,
            pady=15,
            command=lambda: self.state.show_screen(ProfileScreen)
        ).grid(row=1, column=0, columnspan=2, pady=10)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
