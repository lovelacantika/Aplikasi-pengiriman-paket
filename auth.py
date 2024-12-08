from tkinter import messagebox
from utils import load_json, save_json
from menu import main_menu
import json

def login(username, password, root, data_path="data/user.json"):
    """Fungsi untuk login."""
    data_path = ("user.json")
    data = load_json(data_path)
    if not data:
        return False
    for user in range(len(data)):
        if data[user]["username"] == username and data[user]["password"] == password:
            return True

    messagebox.showerror("Login Gagal", "Username atau password salah!")
    return False

def register(username, password, data_path="data/user.json"):
    """Fungsi untuk registrasi.""" 
    file_path = "user.json"
    if not username or not password:
        messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
        return False

    data = load_json(file_path)

    for user in range(len(data)):
        if data[user]["username"] == username:
            messagebox.showerror("Error", "Username sudah digunakan!")
            return False
        
    data.append({"username": username, "password": password})
    save_json(data, file_path)
    return True


