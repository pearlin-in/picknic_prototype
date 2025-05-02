import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import json
import os
from datetime import datetime
import webbrowser
from io import BytesIO
import requests
import webbrowser


class PicknicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Picknic")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFF5EB")  # Creamy background

        # User data
        self.current_user = None
        self.user_data = {}
        self.stamps = []
        self.memories = []
        self.load_sample_stamps()

        # UI colors
        self.colors = {
            "primary": "#FF9AA2",  # Pink
            "secondary": "#FFB7B2",  # Light pink
            "accent": "#FFDAC1",  # Peach
            "background": "#FFF5EB",  # Cream
            "text": "#5A3921",  # Brown
            "highlight": "#E2F0CB",  # Mint
            "stamp_border": "#5A3921"  # Dark brown for stamp edges
        }

        # Create navigation frame
        self.nav_frame = tk.Frame(root, bg=self.colors["primary"], height=60)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Home", self.show_home),
            ("🎯 Hangout", self.show_hangout),
            ("✉️ Mail", self.show_mail),
            ("👤 Me", self.show_profile)
        ]

        for text, command in nav_items:
            btn = tk.Button(
                self.nav_frame,
                text=text,
                font=("Courier", 12, "bold"),
                bg=self.colors["primary"],
                fg=self.colors["text"],
                bd=0,
                activebackground=self.colors["secondary"],
                activeforeground=self.colors["text"],
                command=command
            )
            btn.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
            self.nav_buttons[text] = btn

        # Main content frame
        self.main_frame = tk.Frame(root, bg=self.colors["background"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Start with login screen
        self.show_login()

    def clear_main_frame(self):
        """Clear the main content area"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        """Show login/register screen"""
        self.clear_main_frame()

        # Container frame
        container = tk.Frame(self.main_frame, bg=self.colors["background"])
        container.pack(expand=True, pady=50)

        # Title
        title = tk.Label(
            container,
            text="Welcome to Picknic!",
            font=("Courier", 24, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        title.pack(pady=20)

        # Subtitle
        subtitle = tk.Label(
            container,
            text="Your cute hangout planner",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        subtitle.pack(pady=5)

        # Login form
        form_frame = tk.Frame(container, bg=self.colors["background"])
        form_frame.pack(pady=30)

        # Username
        tk.Label(
            form_frame,
            text="Username:",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).grid(row=0, column=0, pady=5, sticky="e")

        self.username_entry = tk.Entry(
            form_frame,
            font=("Courier", 12),
            bg="white",
            fg=self.colors["text"],
            width=25
        )
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)

        # Password
        tk.Label(
            form_frame,
            text="Password:",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).grid(row=1, column=0, pady=5, sticky="e")

        self.password_entry = tk.Entry(
            form_frame,
            font=("Courier", 12),
            bg="white",
            fg=self.colors["text"],
            show="*",
            width=25
        )
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)

        # Buttons
        btn_frame = tk.Frame(container, bg=self.colors["background"])
        btn_frame.pack(pady=20)

        login_btn = tk.Button(
            btn_frame,
            text="Login",
            font=("Courier", 12, "bold"),
            bg=self.colors["accent"],
            fg=self.colors["text"],
            padx=20,
            pady=5,
            command=self.handle_login
        )
        login_btn.pack(side=tk.LEFT, padx=10)

        register_btn = tk.Button(
            btn_frame,
            text="Register",
            font=("Courier", 12),
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            padx=20,
            pady=5,
            command=self.handle_register
        )
        register_btn.pack(side=tk.LEFT, padx=10)

    def handle_login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror(
                "Error", "Please enter both username and password")
            return

        # Check if user exists
        if os.path.exists(f"user_{username}.json"):
            with open(f"user_{username}.json", "r") as f:
                self.user_data = json.load(f)

            # In a real app, verify password hash
            if password == self.user_data["password"]:
                self.current_user = username
                self.memories = self.user_data.get("memories", [])
                self.show_home()
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "User not found")

    def handle_register(self):
        """Handle new user registration"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror(
                "Error", "Please enter both username and password")
            return

        if os.path.exists(f"user_{username}.json"):
            messagebox.showerror("Error", "Username already exists")
            return

        # Create new user
        self.user_data = {
            "username": username,
            "password": password,  # In real app, hash this
            "memories": [],
            "profile_pic": "",
            "achievements": []
        }

        with open(f"user_{username}.json", "w") as f:
            json.dump(self.user_data, f)

        self.current_user = username
        self.show_home()

    def save_user_data(self):
        """Save user data to file"""
        if self.current_user:
            self.user_data["memories"] = self.memories
            with open(f"user_{self.current_user}.json", "w") as f:
                json.dump(self.user_data, f)

    def show_home(self):
        """Show the home screen"""
        if not self.current_user:
            self.show_login()
            return

        self.clear_main_frame()

        # Welcome message
        welcome_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        welcome_frame.pack(pady=50, fill=tk.X)

        tk.Label(
            welcome_frame,
            text=f"Welcome back, {self.current_user}!",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack()

        tk.Label(
            welcome_frame,
            text="What would you like to do today?",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)

        # Options
        options_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        options_frame.pack(pady=30)

        # Hangout button
        hangout_btn = tk.Button(
            options_frame,
            text="🎯 Find a Hangout Spot",
            font=("Courier", 14, "bold"),
            bg=self.colors["accent"],
            fg=self.colors["text"],
            padx=30,
            pady=15,
            command=self.show_hangout
        )
        hangout_btn.grid(row=0, column=0, padx=20, pady=10)

        # Mail button
        mail_btn = tk.Button(
            options_frame,
            text="✉️ Check Your Mail",
            font=("Courier", 14, "bold"),
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            padx=30,
            pady=15,
            command=self.show_mail
        )
        mail_btn.grid(row=0, column=1, padx=20, pady=10)

        # Recent memories
        if self.memories:
            tk.Label(
                self.main_frame,
                text="Your Recent Adventures",
                font=("Courier", 14, "underline"),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack(pady=20)

            recent_frame = tk.Frame(
                self.main_frame, bg=self.colors["background"])
            recent_frame.pack()

            # Show last 3 memories
            for memory in self.memories[-3:]:
                self.create_memory_letter(recent_frame, memory)

    def show_hangout(self):
        """Show the hangout spot finder"""
        if not self.current_user:
            self.show_login()
            return

        self.clear_main_frame()

        # Title
        tk.Label(
            self.main_frame,
            text="Find Your Perfect Hangout",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)

        # Description
        tk.Label(
            self.main_frame,
            text="Answer a few questions to find spots that match your vibe!",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)

        # Start quiz button
        start_btn = tk.Button(
            self.main_frame,
            text="Start Vibe Quiz",
            font=("Courier", 14, "bold"),
            bg=self.colors["accent"],
            fg=self.colors["text"],
            padx=30,
            pady=10,
            command=self.start_quiz
        )
        start_btn.pack(pady=30)

        # Or browse all stamps
        tk.Label(
            self.main_frame,
            text="Or browse all available spots:",
            font=("Courier", 10),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)

        browse_btn = tk.Button(
            self.main_frame,
            text="Browse Stamps",
            font=("Courier", 12),
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            padx=20,
            pady=5,
            command=self.browse_stamps
        )
        browse_btn.pack(pady=10)

    def start_quiz(self):
        """Start the hangout spot quiz"""
        self.clear_main_frame()

        # Quiz questions
        self.quiz_questions = [
            {
                "question": "What's your mood today?",
                "options": [
                    "😌 Chill & Relaxed",
                    "🎉 Fun & Energetic",
                    "🧠 Cultural/Intellectual",
                    "🏄 Adventure"
                ]
            },
            {
                "question": "Who's coming with you?",
                "options": [
                    "Just me or +1",
                    "Small group (3-5)",
                    "Big group (6+)"
                ]
            },
            {
                "question": "What's your budget?",
                "options": [
                    "💰 Budget (under AED 50)",
                    "💵 Moderate (AED 50-150)",
                    "💸 Splurge (over AED 150)"
                ]
            }
        ]

        self.quiz_answers = {}
        self.current_question = 0

        self.show_quiz_question()

    def show_quiz_question(self):
        """Show the current quiz question"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if self.current_question >= len(self.quiz_questions):
            self.show_quiz_results()
            return

        question = self.quiz_questions[self.current_question]

        # Question text
        tk.Label(
            self.main_frame,
            text=question["question"],
            font=("Courier", 16, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=30)

        # Options
        options_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        options_frame.pack(pady=20)

        for i, option in enumerate(question["options"]):
            btn = tk.Button(
                options_frame,
                text=option,
                font=("Courier", 12),
                bg=self.colors["accent"],
                fg=self.colors["text"],
                padx=20,
                pady=10,
                width=25,
                command=lambda opt=option: self.record_quiz_answer(opt)
            )
            btn.grid(row=i, column=0, pady=5)

    def record_quiz_answer(self, answer):
        """Record the answer and move to next question"""
        question = self.quiz_questions[self.current_question]["question"]
        self.quiz_answers[question] = answer
        self.current_question += 1
        self.show_quiz_question()

    def show_quiz_results(self):
        """Show the quiz results (top 3 recommendations)"""
        self.clear_main_frame()

        # Title
        tk.Label(
            self.main_frame,
            text="Your Perfect Matches",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)

        # Description
        tk.Label(
            self.main_frame,
            text="Based on your answers, we found these spots for you:",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)

        # Get recommendations (filter stamps based on answers)
        filtered_stamps = self.filter_stamps_by_answers()
        self.recommendations = random.sample(
            filtered_stamps, min(3, len(filtered_stamps)))

        # Display recommendations
        rec_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        rec_frame.pack(pady=20)

        for i, stamp in enumerate(self.recommendations):
            frame = tk.Frame(
                rec_frame,
                bg="white",
                padx=15,
                pady=15,
                highlightbackground=self.colors["primary"],
                highlightthickness=2
            )
            frame.grid(row=i, column=0, pady=10, sticky="ew")

            # Stamp title
            tk.Label(
                frame,
                text=stamp["title"],
                font=("Courier", 14, "bold"),
                bg="white"
            ).pack(anchor="w")

            # Description
            tk.Label(
                frame,
                text=stamp["description"],
                font=("Courier", 10),
                bg="white",
                wraplength=400
            ).pack(anchor="w", pady=5)

            # Details
            details = f"📍 {stamp['location']} | 💰 {stamp['budget']} | ⏱️ {stamp['duration']}"
            tk.Label(
                frame,
                text=details,
                font=("Courier", 9),
                bg="white"
            ).pack(anchor="w")

            # Buttons
            btn_frame = tk.Frame(frame, bg="white")
            btn_frame.pack(anchor="w", pady=10)

            # Choose button
            tk.Button(
                btn_frame,
                text="Choose This Spot",
                font=("Courier", 10),
                bg=self.colors["accent"],
                fg="white",
                command=lambda s=stamp: self.select_stamp(s)
            ).pack(side=tk.LEFT, padx=5)

            # More info button
            tk.Button(
                btn_frame,
                text="More Info",
                font=("Courier", 10),
                bg=self.colors["secondary"],
                fg="white",
                command=lambda u=stamp["url"]: webbrowser.open(u)
            ).pack(side=tk.LEFT, padx=5)

    def filter_stamps_by_answers(self):
        """Filter stamps based on quiz answers"""
        # In a real app, this would be more sophisticated
        # Here we just randomly select some stamps
        return random.sample(self.stamps, min(5, len(self.stamps)))

    def select_stamp(self, stamp):
        """Select a stamp and open memory creation"""
        self.current_stamp = stamp
        self.create_memory()

    def create_memory(self):
        """Create a memory for the selected stamp"""
        self.clear_main_frame()

        # Title
        tk.Label(
            self.main_frame,
            text=f"✉️ New Memory: {self.current_stamp['title']}",
            font=("Courier", 18, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)

        # Memory form
        form_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        form_frame.pack(pady=20)

        # Date
        tk.Label(
            form_frame,
            text="Date:",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).grid(row=0, column=0, pady=5, sticky="e")

        self.memory_date = tk.Entry(
            form_frame,
            font=("Courier", 12),
            width=20
        )
        self.memory_date.grid(row=0, column=1, pady=5, padx=10)
        self.memory_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Image
        self.memory_image_path = ""

        tk.Label(
            form_frame,
            text="Photo:",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).grid(row=1, column=0, pady=5, sticky="ne")

        img_btn_frame = tk.Frame(form_frame, bg=self.colors["background"])
        img_btn_frame.grid(row=1, column=1, pady=5, padx=10, sticky="w")

        tk.Button(
            img_btn_frame,
            text="Upload Photo",
            font=("Courier", 10),
            bg=self.colors["accent"],
            fg="white",
            command=self.upload_memory_image
        ).pack(side=tk.LEFT)

        self.img_status = tk.Label(
            img_btn_frame,
            text="No image selected",
            font=("Courier", 8),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.img_status.pack(side=tk.LEFT, padx=10)

        # Notes
        tk.Label(
            form_frame,
            text="Notes:",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).grid(row=2, column=0, pady=5, sticky="ne")

        self.memory_notes = tk.Text(
            form_frame,
            font=("Courier", 11),
            width=40,
            height=10,
            wrap=tk.WORD
        )
        self.memory_notes.grid(row=2, column=1, pady=5, padx=10)

        # Save button
        btn_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Save Memory",
            font=("Courier", 12, "bold"),
            bg=self.colors["primary"],
            fg="white",
            padx=20,
            pady=5,
            command=self.save_memory
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=("Courier", 12),
            bg=self.colors["secondary"],
            fg="white",
            padx=20,
            pady=5,
            command=self.show_hangout
        ).pack(side=tk.LEFT, padx=10)

    def upload_memory_image(self):
        """Upload an image for the memory"""
        filepath = filedialog.askopenfilename(
            title="Select a photo",
            filetypes=(("Image files", "*.jpg *.jpeg *.png"),
                       ("All files", "*.*"))
        )

        if filepath:
            try:
                # Just store the path for now
                self.memory_image_path = filepath
                self.img_status.config(text="Image selected!")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Could not load image: {str(e)}")

    def save_memory(self):
        """Save the memory to the user's collection"""
        notes = self.memory_notes.get("1.0", tk.END).strip()
        date = self.memory_date.get()

        if not notes:
            messagebox.showwarning(
                "Warning", "Please add some notes about your memory")
            return

        memory = {
            "stamp_id": self.current_stamp["id"],
            "stamp_title": self.current_stamp["title"],
            "date": date,
            "notes": notes,
            "image_path": self.memory_image_path
        }

        self.memories.append(memory)
        self.save_user_data()

        messagebox.showinfo("Success", "Memory saved to your mail!")
        self.show_mail()

    def show_mail(self):
        """Show the user's saved memories (mail)"""
        if not self.current_user:
            self.show_login()
            return

        self.clear_main_frame()

        # Title
        tk.Label(
            self.main_frame,
            text="✉️ Your Mail",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)

        if not self.memories:
            # No memories yet
            tk.Label(
                self.main_frame,
                text="No memories yet!\nFind a hangout spot to start collecting.",
                font=("Courier", 12),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack(pady=50)
            return

        # Create scrollable frame for memories
        canvas = tk.Canvas(
            self.main_frame, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["background"])

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Display each memory as a "letter"
        for memory in reversed(self.memories):  # Show newest first
            self.create_memory_letter(scrollable_frame, memory)

    def create_memory_letter(self, parent, memory):
        """Create a letter-style memory widget"""
        # Main letter frame
        letter_frame = tk.Frame(
            parent,
            bg="white",
            padx=20,
            pady=20,
            highlightbackground=self.colors["primary"],
            highlightthickness=1
        )
        letter_frame.pack(fill=tk.X, padx=20, pady=10)

        # Stamp preview (top right)
        stamp_frame = tk.Frame(letter_frame, bg="white")
        stamp_frame.pack(anchor="ne")

        # Find the stamp data
        stamp = next(
            (s for s in self.stamps if s["id"] == memory["stamp_id"]), None)

        if stamp:
            tk.Label(
                stamp_frame,
                text=stamp["title"],
                font=("Courier", 10, "bold"),
                bg="white"
            ).pack(anchor="e")

            tk.Label(
                stamp_frame,
                text=f"📍 {stamp['location']}",
                font=("Courier", 8),
                bg="white"
            ).pack(anchor="e")

        # Date
        tk.Label(
            letter_frame,
            text=f"📅 {memory['date']}",
            font=("Courier", 9),
            bg="white"
        ).pack(anchor="w", pady=5)

        # Image if available
        if memory["image_path"] and os.path.exists(memory["image_path"]):
            try:
                img = Image.open(memory["image_path"])
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)

                img_label = tk.Label(letter_frame, image=photo, bg="white")
                img_label.image = photo  # Keep reference
                img_label.pack(pady=10)
            except Exception as e:
                print(f"Error loading image: {e}")

        # Notes
        notes_frame = tk.Frame(letter_frame, bg="white")
        notes_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            notes_frame,
            text=memory["notes"],
            font=("Courier", 10),
            bg="white",
            wraplength=600,
            justify="left"
        ).pack(anchor="w")

    def show_profile(self):
        """Show user profile"""
        if not self.current_user:
            self.show_login()
            return

        self.clear_main_frame()

        # Title
        tk.Label(
            self.main_frame,
            text=f"👤 {self.current_user}'s Profile",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)

        # Profile picture
        self.profile_pic_frame = tk.Frame(
            self.main_frame, bg=self.colors["background"])
        self.profile_pic_frame.pack(pady=20)

        # Load profile pic if exists
        profile_pic_path = self.user_data.get("profile_pic", "")

        if profile_pic_path and os.path.exists(profile_pic_path):
            try:
                img = Image.open(profile_pic_path)
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)

                self.profile_pic_label = tk.Label(
                    self.profile_pic_frame,
                    image=photo,
                    bg=self.colors["background"]
                )
                self.profile_pic_label.image = photo
                self.profile_pic_label.pack()
            except Exception as e:
                print(f"Error loading profile pic: {e}")
                self.show_default_profile_pic()
        else:
            self.show_default_profile_pic()

        # Upload button
        tk.Button(
            self.profile_pic_frame,
            text="Upload Profile Picture",
            font=("Courier", 10),
            bg=self.colors["accent"],
            fg="white",
            command=self.upload_profile_pic
        ).pack(pady=10)

        # Stats
        stats_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        stats_frame.pack(pady=20)

        tk.Label(
            stats_frame,
            text=f"Memories Collected: {len(self.memories)}",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=5)

        tk.Label(
            stats_frame,
            text=f"Stamps Collected: {len(set(m['stamp_id'] for m in self.memories))}",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=5)

        # Logout button
        tk.Button(
            self.main_frame,
            text="Logout",
            font=("Courier", 12),
            bg=self.colors["secondary"],
            fg="white",
            padx=20,
            pady=5,
            command=self.logout
        ).pack(pady=30)

    def show_default_profile_pic(self):
        """Show default profile picture"""
        # Create a simple colored circle as default pic
        self.profile_pic_label = tk.Label(
            self.profile_pic_frame,
            text=self.current_user[0].upper(),  # First initial
            font=("Courier", 36, "bold"),
            bg=self.colors["primary"],
            fg="white",
            width=4,
            height=2,
            relief="solid",
            bd=0
        )
        self.profile_pic_label.pack()

    def upload_profile_pic(self):
        """Upload a profile picture"""
        filepath = filedialog.askopenfilename(
            title="Select a profile picture",
            filetypes=(("Image files", "*.jpg *.jpeg *.png"),
                       ("All files", "*.*"))
        )

        if filepath:
            try:
                img = Image.open(filepath)
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)

                self.profile_pic_label.config(image=photo)
                self.profile_pic_label.image = photo

                # Save to user data
                self.user_data["profile_pic"] = filepath
                self.save_user_data()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Could not load image: {str(e)}")

    def create_stamp_image(self, stamp_data, size=(200, 150)):
        """Create a postage stamp image with decorative border"""
        # Create blank image
        stamp = Image.new("RGB", size, "#FFF5EB")
        draw = ImageDraw.Draw(stamp)

        # Draw decorative border (scalloped edges)
        border_color = self.colors["stamp_border"]

        # Draw the main rectangle
        draw.rectangle([5, 5, size[0]-5, size[1]-5],
                       outline=border_color, width=2)

        # Draw scalloped edges
        radius = 8
        for x in range(10, size[0]-10, radius*2):
            # Top edge
            draw.arc([x, 0, x+radius*2, radius*2], 180,
                     360, fill=border_color, width=2)
            # Bottom edge
            draw.arc([x, size[1]-radius*2, x+radius*2, size[1]],
                     0, 180, fill=border_color, width=2)

        for y in range(10, size[1]-10, radius*2):
            # Left edge
            draw.arc([0, y, radius*2, y+radius*2], 270,
                     90, fill=border_color, width=2)
            # Right edge
            draw.arc([size[0]-radius*2, y, size[0], y+radius*2],
                     90, 270, fill=border_color, width=2)

        # Add corner decorations
        draw.rectangle([0, 0, radius, radius], outline=border_color, width=2)
        draw.rectangle([size[0]-radius, 0, size[0], radius],
                       outline=border_color, width=2)
        draw.rectangle([0, size[1]-radius, radius, size[1]],
                       outline=border_color, width=2)
        draw.rectangle([size[0]-radius, size[1]-radius, size[0],
                       size[1]], outline=border_color, width=2)

        if "image_path" in stamp_data:
            try:
                img = Image.open(stamp_data["image_path"])
                img.thumbnail((200, 110))

            # Centers the image
                x_offset = (size[0] - img.width) // 2
                y_offset = 18
                stamp.paste(img, (x_offset, y_offset))
            except Exception as e:
                print(f"Error loading image for {stamp_data['title']}: {e}")

        # Add "PICKNIC" text at bottom (like real stamps)
        draw.text((size[0]//2, size[1]-12), "PICKNIC", fill=border_color,
                  anchor="ms", font=ImageFont.load_default())

        return stamp

    def create_stamp_widget(self, parent, stamp_data):
        """Create a beautiful postage stamp widget"""
        frame = tk.Frame(
            parent,
            bg=self.colors["background"],
            padx=10,
            pady=10
        )

        # Create the stamp image
        stamp_img = self.create_stamp_image(stamp_data)
        photo = ImageTk.PhotoImage(stamp_img)

        # Stamp image label
        stamp_label = tk.Label(
            frame,
            image=photo,
            bg=self.colors["background"],
            bd=0
        )
        stamp_label.image = photo  # Keep reference
        stamp_label.pack()

        # Stamp title
        title_label = tk.Label(
            frame,
            text=stamp_data["title"],
            font=("Courier", 10, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"],
            wraplength=180
        )
        title_label.pack(pady=(5, 0))

        # Stamp location
        loc_label = tk.Label(
            frame,
            text=f"📍 {stamp_data['location']}",
            font=("Courier", 8),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        loc_label.pack()

        # Stamp budget
        budget_label = tk.Label(
            frame,
            text=f"💰 {stamp_data['budget']}",
            font=("Courier", 8),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        budget_label.pack()

        return frame

    def browse_stamps(self):
        """Browse all available stamps with beautiful layout"""
        self.clear_main_frame()

        # Title
        tk.Label(
            self.main_frame,
            text="Stamp Collection",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)

        # Description
        tk.Label(
            self.main_frame,
            text="Browse all available hangout spots in our stamp collection:",
            font=("Courier", 10),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=5)

        # Create stamp gallery
        gallery_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        gallery_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Create a canvas for scrolling
        canvas = tk.Canvas(
            gallery_frame, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            gallery_frame, orient="vertical", command=canvas.yview)
        stamps_container = tk.Frame(canvas, bg=self.colors["background"])

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.create_window((0, 0), window=stamps_container, anchor="nw")

        stamps_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        # Display stamps in a grid
        for i, stamp in enumerate(self.stamps):
            row = i // 3
            col = i % 3

            stamp_frame = self.create_stamp_widget(stamps_container, stamp)
            stamp_frame.grid(row=row, column=col, padx=15, pady=15)

            self.add_hover_effect(
                stamp_frame, highlight_color="#FFFFFF", default_color=self.colors["background"])
            # Add click event to select stamp
            stamp_frame.bind("<Button-1>", lambda e,
                             s=stamp: self.select_stamp(s))
            for child in stamp_frame.winfo_children():
                child.bind("<Button-1>", lambda e,
                           s=stamp: self.select_stamp(s))

        # If no stamps found (shouldn't happen but just in case)
        if not self.stamps:
            tk.Label(
                stamps_container,
                text="No stamps available at the moment",
                font=("Courier", 12),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack(pady=50)

    def add_hover_effect(self, widget, highlight_color="#FFFFFF", default_color=None):
        """Adds hover effect to a widget"""
        default_color = default_color or widget["bg"]

        def on_enter(event):
            widget.config(bg=highlight_color)
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=highlight_color)

        def on_leave(event):
            widget.config(bg=default_color)
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=default_color)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def logout(self):
        """Log out the current user"""
        self.save_user_data()
        self.current_user = None
        self.user_data = {}
        self.memories = []
        self.show_login()

    def load_sample_stamps(self):
        """Load sample stamp data"""
        self.stamps = [
            {
                "id": "ST-001",
                "title": "Sunset Beach Picnic",
                "description": "Enjoy a romantic picnic as the sun sets over the water",
                "location": "Corniche Beach",
                "budget": "AED 50-100",
                "duration": "2-3 hours",
                "category": "Romantic",
                "tags": ["outdoor", "couples", "evening"],
                "url": "https://g.co/kgs/1sy6Mpv",
                "image_path": "../picknic/picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-002",
                "title": "Art Cafe Hangout",
                "description": "Creative space with coffee, art exhibits, and board games",
                "location": "Al Bateen",
                "budget": "AED 30-80",
                "duration": "1-2 hours",
                "category": "Creative",
                "tags": ["indoor", "friends", "daytime"],
                "url": "https://g.co/kgs/qD3MNXi",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-003",
                "title": "Desert Stargazing",
                "description": "Evening desert trip with telescope and traditional dinner",
                "location": "Liwa Desert",
                "budget": "AED 150-300",
                "duration": "4-5 hours",
                "category": "Adventure",
                "tags": ["outdoor", "group", "evening"],
                "url": "https://g.co/kgs/S13Swcy",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-004",
                "title": "Vintage Arcade",
                "description": "Retro arcade with classic games and milkshakes",
                "location": "Yas Island",
                "budget": "AED 60-120",
                "duration": "1-3 hours",
                "category": "Fun",
                "tags": ["indoor", "friends", "anytime"],
                "url": "https://g.co/kgs/Ky4vJE3",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-005",
                "title": "Bookstore Cafe",
                "description": "Cozy bookstore with reading nooks and great coffee",
                "location": "Al Reem Island",
                "budget": "AED 20-60",
                "duration": "1-2 hours",
                "category": "Quiet",
                "tags": ["indoor", "solo", "daytime"],
                "url": "https://g.co/kgs/1LPHzeV",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-006",
                "title": "Kayaking Adventure",
                "description": "Explore mangroves by kayak with guided tour",
                "location": "Eastern Mangroves",
                "budget": "AED 100-200",
                "duration": "2-3 hours",
                "category": "Active",
                "tags": ["outdoor", "group", "daytime"],
                "url": "https://g.co/kgs/8pGmG8i",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-007",
                "title": "Rooftop Lounge",
                "description": "Chic rooftop with city views and cocktails",
                "location": "Downtown Abu Dhabi",
                "budget": "AED 80-200",
                "duration": "2-4 hours",
                "category": "Luxury",
                "tags": ["outdoor", "couples", "evening"],
                "url": "https://g.co/kgs/j6UD71p",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-008",
                "title": "DIY Pottery Studio",
                "description": "Create your own pottery with expert guidance",
                "location": "Al Khalidiyah",
                "budget": "AED 70-150",
                "duration": "1-2 hours",
                "category": "Creative",
                "tags": ["indoor", "friends", "daytime"],
                "url": "https://g.co/kgs/kVXCuQY",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-009",
                "title": "Secret Garden Cafe",
                "description": "Hidden garden cafe with homemade treats",
                "location": "Al Nahyan",
                "budget": "AED 40-90",
                "duration": "1-2 hours",
                "category": "Chill",
                "tags": ["outdoor", "any", "daytime"],
                "url": "https://g.co/kgs/swwiqSv",
                "image_path": "../picknic/assets/images/corniche.jpg"
            },
            {
                "id": "ST-010",
                "title": "Night Market",
                "description": "Evening market with local crafts and street food",
                "location": "Hazza Bin Zayed Stadium",
                "budget": "AED 30-100",
                "duration": "1-3 hours",
                "category": "Cultural",
                "tags": ["outdoor", "group", "evening"],
                "url": "https://g.co/kgs/WAc5w3S",
            }
        ]


if __name__ == "__main__":
    root = tk.Tk()
    app = PicknicApp(root)
    root.mainloop()
