from tkinter import messagebox
from utils import load_json, save_json
from menu import main_menu

def login(username, password, root, data_path="data/user.json"):
    """Fungsi untuk login."""
    data = load_json(data_path)
    if not data:
        return False

    for user in data.get("users", []):
        if user["username"] == username and user["password"] == password:
            return True

    messagebox.showerror("Login Gagal", "Username atau password salah!")
    return False

def register(username, password, data_path="data/user.json"):
    """Fungsi untuk registrasi.""" 
    file_path = "users.json"
    if not username or not password:
        messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
        return False

    data = load_json(data_path)
    if not data:
        data = {"users": []}

    for user in data["users"]:
        if user["username"] == username:
            messagebox.showerror("Error", "Username sudah digunakan!")
            return False

    data["users"].append({"username": username, "password": password})
    save_json(data, file_path)
    return True


