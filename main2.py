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
        '''
        self.colors = {
            "primary": "#FF9AA2",  # Pink
            "secondary": "#FFB7B2",  # Light pink
            "accent": "#FFDAC1",  # Peach
            "background": "#FFF5EB",  # Cream
            "text": "#5A3921",  # Brown
            "highlight": "#E2F0CB",  # Mint
            "stamp_border": "#5A3921"  # Dark brown for stamp edges
        }
        '''
        self.colors = {
        "primary": "#3A6EA5",
        "secondary": "#739FD6",
        "accent": "#F5EBDD",
        "background": "#FFF5EB",
        "text": "#2E2E2E",
        "highlight": "#D1E8E2",
        "stamp_border": "#2E2E2E"
        } # Changed the colours a bit so it's more readable
        
        # Create navigation frame
        self.nav_frame = tk.Frame(root, bg=self.colors["primary"], height=60)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Home", self.show_home),
            ("🎯 Hangout", self.show_hangout),
            ("🌍 Explore", self.show_explore),
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

    def show_explore(self):
        """Show all registered users"""
        if not self.current_user:
            self.show_login()
            return
        
        self.clear_main_frame()
        self.main_frame.explore_container = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.main_frame.explore_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        # Title
        tk.Label(
            self.main_frame,
            text="🌍 Explore Users",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)
        
        # Container for user cards
        container = tk.Frame(self.main_frame, bg=self.colors["background"])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create scrollable canvas
        canvas = tk.Canvas(container, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["background"])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Get all user files
        user_files = [f for f in os.listdir() if f.startswith("user_") and f.endswith(".json")]
        
        if not user_files:
            tk.Label(
                scrollable_frame,
                text="No other users found yet!",
                font=("Courier", 14),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack(pady=50)
            return
        
        # Load and display users
        row, col = 0, 0
        for user_file in user_files:
            try:
                with open(user_file, "r") as f:
                    user_data = json.load(f)
                    
                # Skip current user
                if user_data["username"] == self.current_user:
                    continue
                    
                # Create user card
                user_card = tk.Frame(
                    scrollable_frame,
                    bg="white",
                    padx=20,
                    pady=20,
                    relief="ridge",
                    bd=2
                )
                user_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                # Profile picture
                profile_pic_path = user_data.get("profile_pic", "")
                if profile_pic_path and os.path.exists(profile_pic_path):
                    try:
                        img = Image.open(profile_pic_path)
                        img.thumbnail((100, 100))
                        photo = ImageTk.PhotoImage(img)
                        pic_label = tk.Label(user_card, image=photo, bg="white")
                        pic_label.image = photo
                        pic_label.pack()
                    except:
                        self.create_default_profile_display(user_card, user_data["username"])
                else:
                    self.create_default_profile_display(user_card, user_data["username"])
                
                # Username
                tk.Label(
                    user_card,
                    text=user_data["username"],
                    font=("Courier", 12, "bold"),
                    bg="white"
                ).pack(pady=5)
                
                # Stats
                stats_frame = tk.Frame(user_card, bg="white")
                stats_frame.pack()
                
                tk.Label(
                    stats_frame,
                    text=f"Memories: {len(user_data.get('memories', []))}",
                    font=("Courier", 10),
                    bg="white"
                ).pack(side=tk.LEFT, padx=5)
                
                tk.Label(
                    stats_frame,
                    text=f"Stamps: {len(set(m['stamp_id'] for m in user_data.get('memories', [])))}",
                    font=("Courier", 10),
                    bg="white"
                ).pack(side=tk.LEFT, padx=5)

                btn_frame = tk.Frame(user_card, bg="white")
                btn_frame.pack(pady=5)

                request_btn = tk.Button(
                    btn_frame,
                    text="Send Friend Request",
                    font=("Courier", 10),
                    bg=self.colors["accent"],
                    fg="white",
                   command=lambda u=user_data["username"]: self.send_friend_request(u))
                request_btn.pack()

                # Immediately check and update button state
                self.update_friend_request_button(request_btn, user_data["username"])
                 # Update grid position
                col += 1
                if col > 2:
                    col = 0
                    row += 1
                    
            except Exception as e:
                print(f"Error loading {user_file}: {e}")

    def check_request_status(self, button, target_username):
        """Check and update button state initially"""
        try:
            with open(f"user_{target_username}.json", "r") as f:
                target_data = json.load(f)
            
            if self.current_user in target_data.get("friend_requests", []):
                button.config(text="✓ Request Sent", state=tk.DISABLED)
            else:
                button.config(text="Send Friend Request", state=tk.NORMAL)
        except Exception as e:
            button.config(state=tk.DISABLED)
            print(f"Error checking request status: {str(e)}")

    def create_default_profile_display(self, parent, username):
        """Create default profile display for explore page"""
        label = tk.Label(
            parent,
            text=username[0].upper(),
            font=("Courier", 24, "bold"),
            bg=self.colors["primary"],
            fg="white",
            width=4,
            height=2
        )
        label.pack()
        return label
    
    def send_friend_request(self, target_username):
        print(f"Sending request from {self.current_user} to {target_username}")
        if target_username == self.current_user:
            return
        
        try:
            # Load target user's data
            with open(f"user_{target_username}.json", "r") as f:
                target_data = json.load(f)
            
            # Check if request already exists
            if self.current_user not in target_data.get("friend_requests", []):
                target_data.setdefault("friend_requests", []).append(self.current_user)
                
                # Save updated data
                with open(f"user_{target_username}.json", "w") as f:
                    json.dump(target_data, f, indent=4)
                
                messagebox.showinfo("Success", f"Friend request sent to {target_username}!")
                # Refresh explore page to update buttons
                self.show_explore()
            else:
                messagebox.showinfo("Info", "Request already sent!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not send request: {str(e)}")

    def update_friend_request_button(self, button, target_username):
        """Update button state based on existing requests"""
        # Load target user's current data
        try:
            with open(f"user_{target_username}.json", "r") as f:
                target_data = json.load(f)
            
            requests = target_data.get("friend_requests", [])
            if self.current_user in requests:
                button.config(text="✓ Request Sent", state=tk.DISABLED)
            else:
                button.config(text="Send Friend Request", state=tk.NORMAL)
        except Exception as e:
            button.config(state=tk.DISABLED)
            print(f"Error updating button: {str(e)}")
    
    def handle_friend_request(self, sender_username, accept):
        """Handle friend request response"""
        try:
            # Update current user's data
            with open(f"user_{self.current_user}.json", "r") as f:
                current_data = json.load(f)
            
            if sender_username in current_data["friend_requests"]:
                current_data["friend_requests"].remove(sender_username)
                
                if accept:
                    current_data["friends"].append(sender_username)
                    # Also add current user to sender's friends
                    with open(f"user_{sender_username}.json", "r") as f:
                        sender_data = json.load(f)
                    sender_data["friends"].append(self.current_user)
                    with open(f"user_{sender_username}.json", "w") as f:
                        json.dump(sender_data, f)
                
                with open(f"user_{self.current_user}.json", "w") as f:
                    json.dump(current_data, f)
                
                messagebox.showinfo("Success", 
                    f"Accepted {sender_username}'s request!" if accept 
                    else f"Rejected {sender_username}'s request.")
                
                self.show_profile()
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not process request: {str(e)}")

    def start_joint_quiz(self):
        """Start joint hangout planning with a friend"""
        if not self.current_user or not self.user_data.get("friends"):
            messagebox.showinfo("Info", "You need friends to plan a joint hangout!")
            return
        
        self.clear_main_frame()
        
        # Select friend
        tk.Label(
            self.main_frame,
            text="👫 Plan Joint Hangout",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)
        
        tk.Label(
            self.main_frame,
            text="Choose a friend to plan with:",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)
        
        friends_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        friends_frame.pack()
        
        for friend in self.user_data.get("friends", []):
            btn = tk.Button(
                friends_frame,
                text=f"Plan with {friend}",
                font=("Courier", 12),
                bg=self.colors["accent"],
                fg="white",
                padx=20,
                pady=10,
                command=lambda f=friend: self.start_joint_quiz_with_friend(f)
            )
            btn.pack(pady=5, fill=tk.X)

    def start_joint_quiz_with_friend(self, friend):
        """Start quiz with selected friend"""
        self.joint_plan = {
            "friend": friend,
            "your_answers": {},
            "friend_answers": {},
            "current_user": "you"
        }
        
        # Load friend's data to get their preferences
        try:
            with open(f"user_{friend}.json", "r") as f:
                self.friend_data = json.load(f)
        except:
            messagebox.showerror("Error", "Could not load friend's data")
            return
        
        self.show_joint_question()

    def show_joint_question(self):
        """Show joint planning questions"""
        self.clear_main_frame()
        
        # Shared questions for both users
        self.joint_questions = [
            {
                "question": "Preferred vibe for the hangout?",
                "options": [
                    "🎭 Cultural Experience",
                    "🍔 Food Adventure",
                    "🌳 Outdoor Activities",
                    "🎮 Casual Hangout"
                ]
            },
            {
                "question": "How much time do you want to spend?",
                "options": [
                    "⏳ 1-2 hours",
                    "⌛ 3-4 hours",
                    "🕒 Whole day"
                ]
            },
            {
                "question": "Budget preference?",
                "options": [
                    "💰 Budget (under AED 100)",
                    "💵 Moderate (AED 100-300)",
                    "💸 Splurge (AED 300+)"
                ]
            }
        ]
        
        if not hasattr(self, 'current_joint_q'):
            self.current_joint_q = 0
        
        if self.current_joint_q >= len(self.joint_questions):
            self.show_joint_results()
            return
        
        # Show whose turn it is
        user = "Your" if self.joint_plan["current_user"] == "you" else f"{self.joint_plan['friend']}'s"
        tk.Label(
            self.main_frame,
            text=f"{user} Preferences:",
            font=("Courier", 16, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)
        
        question = self.joint_questions[self.current_joint_q]
        
        tk.Label(
            self.main_frame,
            text=question["question"],
            font=("Courier", 14),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)
        
        options_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        options_frame.pack()
        
        for option in question["options"]:
            btn = tk.Button(
                options_frame,
                text=option,
                font=("Courier", 12),
                bg=self.colors["secondary"],
                fg=self.colors["text"],
                padx=20,
                pady=10,
                width=25,
                command=lambda opt=option: self.record_joint_answer(opt)
            )
            btn.pack(pady=5)

    def record_joint_answer(self, answer):
        """Store answer and progress through questions"""
        current_user = self.joint_plan["current_user"]
        question = self.joint_questions[self.current_joint_q]["question"]
        
        if current_user == "you":
            self.joint_plan["your_answers"][question] = answer
        else:
            self.joint_plan["friend_answers"][question] = answer
        
        # Move to next question or switch users
        if self.current_joint_q < len(self.joint_questions) - 1:
            self.current_joint_q += 1
        else:
            if current_user == "you":
                # Switch to friend's turn
                self.current_joint_q = 0
                self.joint_plan["current_user"] = "friend"
            else:
                # Both users have answered
                self.current_joint_q = 0
                self.show_joint_results()
                return
        
        self.show_joint_question()

    def show_joint_results(self):
        """Show combined recommendations"""
        self.clear_main_frame()
        
        # Combine preferences
        combined_answers = {
            "vibe": [
                self.joint_plan["your_answers"].get("Preferred vibe for the hangout?"),
                self.joint_plan["friend_answers"].get("Preferred vibe for the hangout?")
            ],
            "time": max(
                self.joint_plan["your_answers"].get("How much time do you want to spend?"),
                self.joint_plan["friend_answers"].get("How much time do you want to spend?")
            ),
            "budget": max(
                self.joint_plan["your_answers"].get("Budget preference?"),
                self.joint_plan["friend_answers"].get("Budget preference?")
            )
        }
        
        # Filter stamps based on combined preferences
        recommendations = []
        for stamp in self.stamps:
            match = 0
            # Vibe matching
            if any(vibe in stamp["category"] for vibe in combined_answers["vibe"]):
                match += 1
            # Time matching
            if stamp["duration"] == combined_answers["time"]:
                match += 1
            # Budget matching
            if stamp["budget"] == combined_answers["budget"]:
                match += 1
            if match >= 2:
                recommendations.append(stamp)
        
        # Display results
        tk.Label(
            self.main_frame,
            text="Perfect Joint Hangout Spots",
            font=("Courier", 20, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=20)
        
        if not recommendations:
            tk.Label(
                self.main_frame,
                text="No perfect matches found, but these might work:",
                font=("Courier", 12),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack()
            recommendations = random.sample(self.stamps, min(3, len(self.stamps)))
        
        rec_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        rec_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(rec_frame, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(rec_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["background"])
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        for stamp in recommendations:
            frame = self.create_joint_stamp_card(scrollable_frame, stamp)
            frame.pack(fill=tk.X, pady=10, padx=20)

    def create_joint_stamp_card(self, parent, stamp):
        """Create special joint hangout card"""
        frame = tk.Frame(
            parent,
            bg="white",
            padx=20,
            pady=20,
            highlightbackground=self.colors["primary"],
            highlightthickness=2
        )
        
        # Title with hearts
        title_frame = tk.Frame(frame, bg="white")
        title_frame.pack(fill=tk.X)
        tk.Label(
            title_frame,
            text="❤️ " + stamp["title"] + " ❤️",
            font=("Courier", 14, "bold"),
            bg="white"
        ).pack(side=tk.LEFT)
        
        # Compatibility info
        comp_frame = tk.Frame(frame, bg="white")
        comp_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            comp_frame,
            text=f"👥 Good for duos | ⏱ {stamp['duration']} | 💰 {stamp['budget']}",
            font=("Courier", 10),
            bg="white"
        ).pack(side=tk.LEFT)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            btn_frame,
            text="Choose Together",
            font=("Courier", 10),
            bg=self.colors["accent"],
            fg="white",
            command=lambda s=stamp: self.save_joint_plan(s)
        ).pack(side=tk.LEFT, padx=5)
        
        return frame

    def save_joint_plan(self, stamp):
        """Save the joint plan for both users"""
        plan_details = {
        "type": "joint",
        "friend": self.joint_plan["friend"],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "stamp_id": stamp["id"],
        "stamp_title": stamp["title"],
        "notes": f"Joint plan with {self.joint_plan['friend']}",
        "status": "pending",
        "scrapbook": [],
        # Add empty image_path for compatibility
        "image_path": ""  
    }
        
         # Save to current user
        if isinstance(self.memories, list):
            self.memories.append(plan_details)
        else:
            self.memories = [plan_details]
        self.save_user_data()
            
        # Save to friend's data
        try:
            with open(f"user_{self.joint_plan['friend']}.json", "r") as f:
                friend_data = json.load(f)
            # Ensure friend's memories is a list
            if not isinstance(friend_data.get("memories", []), list):
                friend_data["memories"] = []
            friend_data["memories"].append(plan_details)
            with open(f"user_{self.joint_plan['friend']}.json", "w") as f:
                json.dump(friend_data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save friend's plan: {str(e)}")
        
        messagebox.showinfo("Success", 
            f"Joint plan saved! {self.joint_plan['friend']} has been notified!")
        self.show_home()
                    
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
     
    def create_default_profile_display(self, parent, username):
        """Create default profile display for explore page"""
        label = tk.Label(
            parent,
            text=username[0].upper(),
            font=("Courier", 24, "bold"),
            bg=self.colors["primary"],
            fg="white",
            width=4,
            height=2
        )
        label.pack()
        return label

    def handle_login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check if user exists
        if os.path.exists(f"user_{username}.json"):
                with open(f"user_{username}.json", "r") as f:
                    self.user_data = json.load(f)
                
                # Ensure memories is a list and repair if needed
                memories = self.user_data.get("memories", [])
                if not isinstance(memories, list):
                    memories = []
                
                # Add missing 'image_path' to old entries
                for memory in memories:
                    if isinstance(memory, dict):
                        memory.setdefault("image_path", "")
                
                self.user_data["memories"] = memories
                self.memories = memories
                
                if password == self.user_data["password"]:
                    self.current_user = username
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
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if os.path.exists(f"user_{username}.json"):
            messagebox.showerror("Error", "Username already exists")
            return
        
        # Create new user
        self.user_data = {
            "username": username,
            "password": password,
            "memories": [],
            "profile_pic": "",
            "achievements": [],
            "friends": [],
            "friend_requests": []  # Add this line
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
            
            recent_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
            recent_frame.pack()
            
            # Show last 3 memories
            if self.memories and isinstance(self.memories, list):
                for memory in self.memories[-3:]:
                    self.create_memory_letter(recent_frame, memory)
            else:
                self.memories = []
    
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

        tk.Label(
            self.main_frame,
            text="Plan with a friend:",
            font=("Courier", 10),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)
        
        tk.Button(
            self.main_frame,
            text="👫 Joint Hangout Planner",
            font=("Courier", 12),
            bg=self.colors["primary"],
            fg="white",
            padx=20,
            pady=5,
            command=self.start_joint_quiz
        ).pack(pady=10)
    
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
        self.recommendations = random.sample(filtered_stamps, min(3, len(filtered_stamps)))
        
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
            filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
        )
        
        if filepath:
            try:
                # Just store the path for now
                self.memory_image_path = filepath
                self.img_status.config(text="Image selected!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def save_memory(self):
        """Save the memory to the user's collection"""
        notes = self.memory_notes.get("1.0", tk.END).strip()
        date = self.memory_date.get()
        
        if not notes:
            messagebox.showwarning("Warning", "Please add some notes about your memory")
            return
        
        memory = {
            "stamp_id": self.current_stamp["id"],
            "stamp_title": self.current_stamp["title"],
            "date": date,
            "notes": notes,
            "image_path": self.memory_image_path
        }
        # Check for duplicates
        if memory not in self.memories:
            if isinstance(self.memories, list):
                self.memories.append(memory)
            else:
                self.memories = [memory]
            self.save_user_data()
            messagebox.showinfo("Success", "Memory saved to your mail!")
        else:
            messagebox.showinfo("Info", "This memory already exists!")
        
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
        canvas = tk.Canvas(self.main_frame, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
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
        if not isinstance(memory, dict):
            return

        # Main frame
        letter_frame = tk.Frame(
            parent,
            bg="white",
            padx=20,
            pady=20,
            highlightbackground=self.colors["primary"],
            highlightthickness=1
        )
        letter_frame.pack(fill=tk.X, padx=20, pady=10)

        # --- Image Section (Top) ---
        image_path = memory.get("image_path", "")
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.thumbnail((200, 200))  # Resize for consistency
                photo = ImageTk.PhotoImage(img)
                
                img_label = tk.Label(letter_frame, image=photo, bg="white")
                img_label.image = photo  # Retain reference
                img_label.pack(pady=10)  # Position image at the top
            except Exception as e:
                print(f"Image load error: {e}")
        elif image_path:  # Path exists but image not found
            print(f"Warning: Image not found at {image_path}")

        # --- Title & Location ---
        title_frame = tk.Frame(letter_frame, bg="white")
        title_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            title_frame,
            text=f"✉️ {memory.get('stamp_title', 'Unnamed Memory')}",
            font=("Courier", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT)

        
        tk.Label(
            letter_frame,
            text=f"📅 {memory.get('date', 'No Date')}",
            font=("Courier", 9),
            bg="white"
        ).pack(anchor="w", pady=5)

        # --- Notes ---
        notes = memory.get("notes", "")
        if notes.strip():
            tk.Label(
                letter_frame,
                text=notes,
                font=("Courier", 10),
                bg="white",
                wraplength=600,
                justify="left"
            ).pack(anchor="w", pady=10)

        # --- Joint Plan Badge (if applicable) ---
        if memory.get("type") == "joint":
            tk.Label(
                letter_frame,
                text=f"👫 Joint Plan with {memory.get('friend', 'Unknown')}",
                font=("Courier", 10, "italic"),
                bg=self.colors["highlight"],
                fg=self.colors["text"]
            ).pack(anchor="w", fill=tk.X, pady=5)
                
    def show_profile(self):
        """Show user profile"""
        if not self.current_user:
            self.show_login()
            return
        
         # Reload fresh data
        with open(f"user_{self.current_user}.json", "r") as f:
            self.user_data = json.load(f)
    
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
        self.profile_pic_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
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
            text=f"Stamps Collected: {len(set(m['stamp_id'] for m in self.memories if isinstance(m, dict)))}",
            font=("Courier", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=5)
        
        # Friend requests
        tk.Label(
            self.main_frame,
            text="Friend Requests",
            font=("Courier", 14, "underline"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)

        # Load current user's friend requests
        with open(f"user_{self.current_user}.json", "r") as f:
            current_user_data = json.load(f)
            
        requests = current_user_data.get("friend_requests", [])

        if not requests:
            tk.Label(
                self.main_frame,
                text="No pending friend requests",
                font=("Courier", 10),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack()
        else:
            req_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
            req_frame.pack()
            
            for req in requests:
                req_entry = tk.Frame(req_frame, bg="white", padx=10, pady=5)
                req_entry.pack(fill=tk.X, pady=2)
                
                tk.Label(
                    req_entry,
                    text=req,
                    font=("Courier", 12),
                    bg="white"
                ).pack(side=tk.LEFT)
                
                tk.Button(
                    req_entry,
                    text="Accept",
                    font=("Courier", 8),
                    bg=self.colors["accent"],
                    fg="white",
                    command=lambda r=req: self.handle_friend_request(r, True)
                ).pack(side=tk.LEFT, padx=5)
                
                tk.Button(
                    req_entry,
                    text="Reject",
                    font=("Courier", 8),
                    bg=self.colors["secondary"],
                    fg="white",
                    command=lambda r=req: self.handle_friend_request(r, False)
                ).pack(side=tk.LEFT)
                # Logout button

        tk.Label(
            self.main_frame,
            text="Friends",
            font=("Courier", 14, "underline"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        ).pack(pady=10)

        friends = self.user_data.get("friends", [])
        if not friends:
            tk.Label(
                self.main_frame,
                text="No friends yet",
                font=("Courier", 10),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack()
        else:
            friends_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
            friends_frame.pack()
            for friend in friends:
                tk.Label(
                    friends_frame,
                    text=f"• {friend}",
                    font=("Courier", 12),
                    bg=self.colors["background"],
                    fg=self.colors["text"]
                ).pack(anchor="w")
                
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
            filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
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
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def create_stamp_image(self, stamp_data, size=(200, 150)):
        """Create a postage stamp image with decorative border"""
        # Create blank image
        stamp = Image.new("RGB", size, "#FFF5EB")
        draw = ImageDraw.Draw(stamp)
        
        # Draw decorative border (scalloped edges)
        border_color = self.colors["stamp_border"]
        
        # Draw the main rectangle
        draw.rectangle([5, 5, size[0]-5, size[1]-5], outline=border_color, width=2)
        
        # Draw scalloped edges
        radius = 8
        for x in range(10, size[0]-10, radius*2):
            # Top edge
            draw.arc([x, 0, x+radius*2, radius*2], 180, 360, fill=border_color, width=2)
            # Bottom edge
            draw.arc([x, size[1]-radius*2, x+radius*2, size[1]], 0, 180, fill=border_color, width=2)
        
        for y in range(10, size[1]-10, radius*2):
            # Left edge
            draw.arc([0, y, radius*2, y+radius*2], 270, 90, fill=border_color, width=2)
            # Right edge
            draw.arc([size[0]-radius*2, y, size[0], y+radius*2], 90, 270, fill=border_color, width=2)
        
        # Add corner decorations
        draw.rectangle([0, 0, radius, radius], outline=border_color, width=2)
        draw.rectangle([size[0]-radius, 0, size[0], radius], outline=border_color, width=2)
        draw.rectangle([0, size[1]-radius, radius, size[1]], outline=border_color, width=2)
        draw.rectangle([size[0]-radius, size[1]-radius, size[0], size[1]], outline=border_color, width=2)
        
        # Add "PICKNIC" text at bottom (like real stamps)
        draw.text((size[0]//2, size[1]-12), "PICKNIC", fill=border_color, anchor="ms", font=ImageFont.load_default())
        
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
        canvas = tk.Canvas(gallery_frame, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(gallery_frame, orient="vertical", command=canvas.yview)
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
            
            # Add click event to select stamp
            stamp_frame.bind("<Button-1>", lambda e, s=stamp: self.select_stamp(s))
            for child in stamp_frame.winfo_children():
                child.bind("<Button-1>", lambda e, s=stamp: self.select_stamp(s))
        
        # If no stamps found (shouldn't happen but just in case)
        if not self.stamps:
            tk.Label(
                stamps_container,
                text="No stamps available at the moment",
                font=("Courier", 12),
                bg=self.colors["background"],
                fg=self.colors["text"]
            ).pack(pady=50)
        
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
                "url": "https://www.timeoutabudhabi.com/beaches/482527-corniche-beach"
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
                "url": "https://www.timeoutabudhabi.com/art/482527-art-cafe"
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
                "url": "https://www.timeoutabudhabi.com/things-to-do/482527-desert-stargazing"
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
                "url": "https://www.timeoutabudhabi.com/things-to-do/482527-vintage-arcade"
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
                "url": "https://www.timeoutabudhabi.com/food-drink/482527-bookstore-cafe"
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
                "url": "https://www.timeoutabudhabi.com/things-to-do/482527-kayaking"
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
                "url": "https://www.timeoutabudhabi.com/bars/482527-rooftop-lounge"
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
                "url": "https://www.timeoutabudhabi.com/art/482527-pottery-studio"
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
                "url": "https://www.timeoutabudhabi.com/food-drink/482527-secret-garden"
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
                "url": "https://www.timeoutabudhabi.com/shopping/482527-night-market"
            }
        ]

if __name__ == "__main__":
    root = tk.Tk()
    app = PicknicApp(root)
    root.mainloop()

