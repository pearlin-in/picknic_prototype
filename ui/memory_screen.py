# for creating and viewing memories
import tkinter as tk
from tkinter import filedialog, messagebox
from core.user_manager import save_user

class MemoryScreen:
    def __init__(self, state):
        self.state = state
        self.root = state.root
        self.img_path = ""

    def show(self):
        self.clear()
        bg = self.state.colors["background"]
        text = self.state.colors["text"]

        tk.Label(self.root, text=f"New Memory: {self.state.current_stamp['title']}", font=("Courier", 18, "bold"), bg=bg, fg=text).pack(pady=20)

        form = tk.Frame(self.root, bg=bg)
        form.pack(pady=20)

        tk.Label(form, text="Date:", font=("Courier", 12), bg=bg, fg=text).grid(row=0, column=0, sticky="e")
        self.date_entry = tk.Entry(form, font=("Courier", 12))
        self.date_entry.grid(row=0, column=1, padx=10)

        tk.Label(form, text="Notes:", font=("Courier", 12), bg=bg, fg=text).grid(row=1, column=0, sticky="ne")
        self.notes = tk.Text(form, font=("Courier", 11), width=40, height=5)
        self.notes.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(form, text="Upload Photo", font=("Courier", 10), bg=self.state.colors["accent"], command=self.upload_image).grid(row=2, column=1, sticky="w", pady=10)
        self.img_label = tk.Label(form, text="No image selected", font=("Courier", 9), bg=bg, fg=text)
        self.img_label.grid(row=2, column=1, sticky="e")

        tk.Button(self.root, text="Save Memory", font=("Courier", 12, "bold"), bg=self.state.colors["primary"], command=self.save).pack(pady=20)

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if path:
            self.img_path = path
            self.img_label.config(text="Image selected")

    def save(self):
        date = self.date_entry.get()
        notes = self.notes.get("1.0", tk.END).strip()
        if not notes:
            messagebox.showerror("Error", "Please write a note")
            return

        mem = {
            "stamp_id": self.state.current_stamp["id"],
            "stamp_title": self.state.current_stamp["title"],
            "date": date,
            "notes": notes,
            "image_path": self.img_path
        }
        self.state.memories.append(mem)
        self.state.user_data["memories"] = self.state.memories
        save_user(self.state.current_user, self.state.user_data)
        messagebox.showinfo("Saved", "Memory saved!")
