from tkinter import Frame, Label, Entry, Button, messagebox
from services.auth import login_user, register_user

def show_login(app):
    app.clear_main_frame()

    frame = Frame(app.main_frame, bg=app.colors['background'])
    frame.pack(expand=True, pady=50)

    Label(frame, text="Login to Picknic", font=("Courier", 24),
          bg=app.colors['background'], fg=app.colors['text']).pack(pady=10)

    username_entry = Entry(frame, font=("Courier", 12))
    username_entry.pack(pady=5)
    username_entry.insert(0, "Username")

    password_entry = Entry(frame, font=("Courier", 12), show='*')
    password_entry.pack(pady=5)
    password_entry.insert(0, "password")

    def handle_login():
        user = login_user(username_entry.get(), password_entry.get())
        if user:
            app.login_success(user)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def handle_register():
        user = register_user(username_entry.get(), password_entry.get())
        if user:
            messagebox.showinfo("Success", "User registered. Please log in.")
        else:
            messagebox.showerror("Error", "Username already exists")

    Button(frame, text="Login", font=("Courier", 12), bg=app.colors['accent'], command=handle_login).pack(pady=5)
    Button(frame, text="Register", font=("Courier", 12), bg=app.colors['secondary'], command=handle_register).pack(pady=5)
