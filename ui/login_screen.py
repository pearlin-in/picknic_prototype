import tkinter as tk
from tkinter import messagebox
from core.user_manager import load_user, save_user, user_exists
from ui.home_screen import HomeScreen
from ui.widgets import create_navbar

class LoginScreen:
    def __init__(self, state):
        self.state = state
        self.root = state.root

    def show(self):
        self.clear()
        bg = self.state.colors["background"]
        text_color = self.state.colors["text"]

        container = tk.Frame(self.root, bg=bg)
        container.pack(expand=True, pady=50)

        tk.Label(container, text="Welcome to Picknic!", font=("Courier", 24, "bold"), bg=bg, fg=text_color).pack(pady=20)
        tk.Label(container, text="Your cute hangout planner", font=("Courier", 12), bg=bg, fg=text_color).pack(pady=5)

        form = tk.Frame(container, bg=bg)
        form.pack(pady=30)

        tk.Label(form, text="Username:", font=("Courier", 12), bg=bg, fg=text_color).grid(row=0, column=0, pady=5, sticky="e")
        self.username_entry = tk.Entry(form, font=("Courier", 12), bg="white", fg=text_color, width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(form, text="Password:", font=("Courier", 12), bg=bg, fg=text_color).grid(row=1, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(form, font=("Courier", 12), bg="white", fg=text_color, show="*", width=25)
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        btns = tk.Frame(container, bg=bg)
        btns.pack(pady=20)

        tk.Button(btns, text="Login", font=("Courier", 12, "bold"), bg=self.state.colors["accent"], fg=text_color, padx=20, pady=5, command=self.login).pack(side=tk.LEFT, padx=10)
        tk.Button(btns, text="Register", font=("Courier", 12), bg=self.state.colors["secondary"], fg=text_color, padx=20, pady=5, command=self.register).pack(side=tk.LEFT, padx=10)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        data = load_user(username)
        if data and data.get("password") == password:
            self.state.current_user = username
            self.state.user_data = data
            self.state.memories = data.get("memories", [])
            self.state.show_screen(HomeScreen)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        if user_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return

        data = {
            "username": username,
            "password": password,
            "memories": [],
            "profile_pic": "",
            "achievements": []
        }
        save_user(username, data)
        self.state.current_user = username
        self.state.user_data = data
        self.state.memories = []
        self.state.show_screen(HomeScreen)