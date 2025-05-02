import tkinter as tk
from core.app_state import AppState
from ui.login_screen import LoginScreen

def main():
    root = tk.Tk()
    state = AppState(root)
    LoginScreen(state).show()
    root.mainloop()

if __name__ == "__main__":
    main()
