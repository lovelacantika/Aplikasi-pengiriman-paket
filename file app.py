import tkinter as tk
from tkinter import messagebox
import json

# Fungsi untuk membaca data dari user.json
def load_data():
    try:
        with open("user.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "File user.json tidak ditemukan!")
        return None

# Fungsi untuk menyimpan data ke user.json
def save_data(updated_data):
    try:
        with open("user.json", "w") as file:
            # Simpan data dengan indentasi agar mudah dibaca
            json.dump(updated_data, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan data: {e}")
        
# Load data dari file JSON
with open("data.json", "r") as file:
    data = json.load(file)

# Fungsi untuk verifikasi login
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    for user in data["users"]:
        if user["username"] == username and user["password"] == password:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
            frame_login.pack_forget()
            frame_pengiriman.pack()
            return
    
    messagebox.showerror("Login Gagal", "Username atau password salah!")

# Fungsi untuk menghitung biaya
def hitung_biaya():
    try:
        pengirim = pengirim_entry.get()
        penerima = penerima_entry.get()
        kota_tujuan = kota_tujuan_var.get()
        berat = float(berat_entry.get())
        
        if kota_tujuan not in data["harga_jarak"]:
            messagebox.showerror("Error", "Kota tujuan tidak valid!")
            return
        
        harga_jarak = data["harga_jarak"][kota_tujuan]
        harga_dasar = berat * 10000
        total_biaya = harga_dasar + harga_jarak
        
        resi_text.set(f"""
        Nama Pengirim: {pengirim}
        Nama Penerima: {penerima}
        Kota Tujuan: {kota_tujuan}
        Berat Paket: {berat} kg
        Biaya Dasar: Rp {harga_dasar}
        Harga Jarak: Rp {harga_jarak}
        Total Biaya: Rp {total_biaya}
        """)
    except ValueError:
        messagebox.showerror("Error", "Masukkan data yang valid!")

# GUI utama
root = tk.Tk()
root.title("Aplikasi Pengiriman Paket")

# Frame Login
frame_login = tk.Frame(root, padx=10, pady=10)
frame_login.pack()

tk.Label(frame_login, text="Username:").grid(row=0, column=0, sticky="w")
username_entry = tk.Entry(frame_login)
username_entry.grid(row=0, column=1)

tk.Label(frame_login, text="Password:").grid(row=1, column=0, sticky="w")
password_entry = tk.Entry(frame_login, show="*")
password_entry.grid(row=1, column=1)

tk.Button(frame_login, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=5)

# Frame Pengiriman
frame_pengiriman = tk.Frame(root, padx=10, pady=10)

tk.Label(frame_pengiriman, text="Nama Pengirim:").grid(row=0, column=0, sticky="w")
pengirim_entry = tk.Entry(frame_pengiriman)
pengirim_entry.grid(row=0, column=1)

tk.Label(frame_pengiriman, text="Nama Penerima:").grid(row=1, column=0, sticky="w")
penerima_entry = tk.Entry(frame_pengiriman)
penerima_entry.grid(row=1, column=1)

tk.Label(frame_pengiriman, text="Kota Tujuan:").grid(row=2, column=0, sticky="w")
kota_tujuan_var = tk.StringVar()
kota_tujuan_menu = tk.OptionMenu(frame_pengiriman, kota_tujuan_var, *data["harga_jarak"].keys())
kota_tujuan_menu.grid(row=2, column=1)

tk.Label(frame_pengiriman, text="Berat (kg):").grid(row=3, column=0, sticky="w")
berat_entry = tk.Entry(frame_pengiriman)
berat_entry.grid(row=3, column=1)

tk.Button(frame_pengiriman, text="Hitung Biaya", command=hitung_biaya).grid(row=4, column=0, columnspan=2, pady=5)

# Frame Resi
frame_resi = tk.Frame(root, padx=10, pady=10)
frame_resi.pack_forget()

resi_text = tk.StringVar()
resi_label = tk.Label(frame_resi, textvariable=resi_text, justify="left")
resi_label.pack()

tk.Button(frame_pengiriman, text="Cetak Resi", command=lambda: frame_resi.pack()).grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()