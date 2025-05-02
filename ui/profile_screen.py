# for viewing/updating user profile
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from core.user_manager import save_user
from ui.widgets import create_navbar

class ProfileScreen:
    def __init__(self, state):
        self.state = state
        self.root = state.root

    def show(self):
        self.clear()
        create_navbar(self.state, self.root)

        bg = self.state.colors["background"]
        text = self.state.colors["text"]

        tk.Label(self.root, text=f"👤 {self.state.current_user}'s Profile", font=("Courier", 20, "bold"), bg=bg, fg=text).pack(pady=20)

        if self.state.user_data.get("profile_pic"):
            try:
                img = Image.open(self.state.user_data["profile_pic"])
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(self.root, image=photo, bg=bg)
                lbl.image = photo
                lbl.pack()
            except:
                pass

        tk.Button(self.root, text="Upload Profile Picture", font=("Courier", 10), bg=self.state.colors["accent"], command=self.upload_pic).pack(pady=10)

        tk.Label(self.root, text=f"Memories Collected: {len(self.state.memories)}", font=("Courier", 12), bg=bg, fg=text).pack(pady=5)
        tk.Label(self.root, text=f"Stamps Visited: {len(set(m['stamp_id'] for m in self.state.memories))}", font=("Courier", 12), bg=bg, fg=text).pack(pady=5)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def upload_pic(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if path:
            self.state.user_data["profile_pic"] = path
            save_user(self.state.current_user, self.state.user_data)
            self.show()