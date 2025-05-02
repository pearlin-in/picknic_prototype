# placeholder for reusable UI widgets (like tamp cards or memory previews)
import tkinter as tk
from ui.home_screen import HomeScreen
from ui.hangout_screen import HangoutScreen
from ui.memory_screen import MemoryScreen
from ui.profile_screen import ProfileScreen

def create_navbar(state, parent):
    colors = state.colors
    nav_frame = tk.Frame(parent, bg=colors["primary"], height=60)
    nav_frame.pack(side=tk.TOP, fill=tk.X)

    buttons = [
        ("🏠 Home", HomeScreen),
        ("🎯 Hangout", HangoutScreen),
        ("✉️ Mail", MemoryScreen),
        ("👤 Me", ProfileScreen)
    ]

    for label, screen in buttons:
        tk.Button(
            nav_frame,
            text=label,
            font=("Courier", 12, "bold"),
            bg=colors["primary"],
            fg=colors["text"],
            bd=0,
            activebackground=colors["secondary"],
            activeforeground=colors["text"],
            command=lambda s=screen: state.show_screen(s)
        ).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)