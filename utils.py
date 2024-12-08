import json
from tkinter import messagebox

def load_json(file_path):
    """Membaca data dari file JSON."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_path} tidak ditemukan!")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", f"File {file_path} rusak atau tidak valid!")
        return None

def save_json(data, file_path):
    """Menyimpan data ke file JSON."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan data: {e}")
    
def load_harga():
    try:
        with open("data/harga.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "File harga.json tidak ditemukan!")
    return None
def load_data():
    try:
        with open("data/user.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "File user.json tidak ditemukan!")
        return None