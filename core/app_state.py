# User session, shared state
class AppState:
    def __init__(self, root):
        self.root = root
        self.root.title("Picknic")
        self.root.geometry("1000x700")
        self.root.configure(bg="#FFF5EB")

        self.current_user = None
        self.user_data = {}
        self.memories = []
        self.colors = {
            "primary": "#FF9AA2",
            "secondary": "#FFB7B2",
            "accent": "#FFDAC1",
            "background": "#FFF5EB",
            "text": "#5A3921",
            "highlight": "#E2F0CB",
            "stamp_border": "#5A3921"
        }
        self.stamps = []
        self.current_stamp = None

    def show_screen(self, ScreenClass):
        for widget in self.root.winfo_children():
            widget.destroy()
        ScreenClass(self).show()