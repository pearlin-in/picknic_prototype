import tkinter as tk
from ui import screens
from models.user import User

class PicknicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Picknic")
        self.root.geometry("1000x700")

        self.current_user = None
        self.user_data = {}

        self.colors = {
            "primary": "#FF9AA2",
            "secondary": "#FFB7B2",
            "accent": "#FFDAC1",
            "background": "#FFF5EB",
            "text": "#5A3921",
            "highlight": "#E2F0CB",
            "stamp_border": "#5A3921"
        }

        self.nav_frame = tk.Frame(root, bg=self.colors["primary"], height=60)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.main_frame = tk.Frame(root, bg=self.colors["background"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.show_login()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_login(self):
        screens.show_login(self)

    def login_success(self, user):
        self.current_user = user.username
        self.user_data = user
        print(f"Logged in as {self.current_user}")  # placeholder for next screen

if __name__ == "__main__":
    root = tk.Tk()
    app = PicknicApp(root)
    root.mainloop()