import tkinter as tk
from auth import login,register
from menu import main_menu

def show_register_window():
    """Jendela registrasi."""
    pass  # Implementasi sama seperti sebelumnya.

def attempt_login():
    username = username_entry.get()
    password = password_entry.get()
    if login(username, password):
        root.destroy()
        main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("670x450")
    root.title("Login Pengiriman Paket")

    tk.Label(root, text="Username:", font=("Arial", 16)).place(x=130, y=125)
    username_entry = tk.Entry(root, font=("Arial", 16))
    username_entry.place(x=300, y=125)

    tk.Label(root, text="Password:", font=("Arial", 16)).place(x=130, y=270)
    password_entry = tk.Entry(root, font=("Arial", 16), show="*")
    password_entry.place(x=300, y=270)

    tk.Button(root, text="Login", command=attempt_login, font=("Arial", 16)).place(x=150, y=375)
    tk.Button(root, text="Register", command=show_register_window, font=("Arial", 16)).place(x=410, y=375)

    root.mainloop()
