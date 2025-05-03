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
        "primary": "#3A6EA5",
        "secondary": "#739FD6",
        "accent": "#F5EBDD",
        "background": "#FFF5EB",
        "text": "#2E2E2E",
        "highlight": "#D1E8E2",
        "stamp_border": "#2E2E2E"
        }
        self.stamps = []
        self.current_stamp = None

    def show_screen(self, ScreenClass):
        for widget in self.root.winfo_children():
            widget.destroy()
        ScreenClass(self).show()