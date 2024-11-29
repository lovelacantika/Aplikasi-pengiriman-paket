Kelas A
Kelompok 10
Daftar Anggota :
I0324017 Lovela Cantika Wardhana / https://github.com/lovelacantika
I0324038 Batra Sandy / @Batrasandy38
I0324042 Daniswara Bharata / @DaniswaraBharata042
# Aplikasi-pengiriman-paket
Aplikasi untuk mencatat biaya dalam pengiriman paket. Aplikasi untuk menyediakan tanggal dan waktu paket diantarkan dan perkiraan sampai di tujuan. Customer mengisi identitas seperti nama dan alamat. Customer akan mendapat output tanggal pengiriman, perkiraan barang sampai, dan biaya pengiriman paket tersebut

Fitur - Fitur : 
1. Pilihan alamat yang nantinya akan dikirim barang
2. Pilihan tanggal pengiriman
3. Rincian Biaya
4. Pilihan Berat

DIAGRAM ALIR
![flow bhara (2)](https://github.com/user-attachments/assets/39448e00-185e-4f5b-8222-04b72f7e9a00)

CODDING 
import json
import tkinter as tk
from tkinter import messagebox

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


# Fungsi untuk login
def login():
    username = username_entry.get()
    password = password_entry.get()
    for user in data["users"]:
        if user["username"] == username and user["password"] == password:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
            root.destroy()
            show_main_window()
            return
    messagebox.showerror("Login Gagal", "Username atau password salah!")

# Fungsi untuk registrasi
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    # Validasi input
    if not username or not password:
        messagebox.showerror("Error", "Username dan password tidak boleh kosong!")
        return

    # Cek apakah username sudah ada
    for user in data["users"]:
        if user["username"] == username:
            messagebox.showerror("Error", "Username sudah digunakan!")
            return

    # Tambahkan pengguna baru ke data
    data["users"].append({"username": username, "password": password})

    # Simpan data ke file JSON
    save_data(data)

    # Beri notifikasi keberhasilan
    messagebox.showinfo("Registrasi Berhasil", "Akun berhasil dibuat! Silakan login.")
    reg_window.destroy()


    # Tambahkan pengguna baru ke data
    data["users"].append({"username": username, "password": password})
    save_data(data)  # Simpan data yang diperbarui ke user.json

    messagebox.showinfo("Registrasi Berhasil", "Akun berhasil dibuat! Silakan login.")
    reg_window.destroy()

# Fungsi untuk menampilkan jendela registrasi
def show_register_window():
    global reg_username_entry, reg_password_entry, reg_window
    reg_window = tk.Toplevel(root)
    reg_window.title("Registrasi")
    
    tk.Label(reg_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    reg_username_entry = tk.Entry(reg_window)
    reg_username_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(reg_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    reg_password_entry = tk.Entry(reg_window, show="*")
    reg_password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Button(reg_window, text="Daftar", command=register).grid(row=2, column=0, columnspan=2, pady=10)

# Fungsi untuk menampilkan jendela utama
def show_main_window():
    global sender_entry, receiver_entry, city_entry, weight_entry
    main_window = tk.Tk()
    main_window.title("Pengiriman Paket")
    
    tk.Label(main_window, text="Nama Pengirim:").grid(row=0, column=0, padx=10, pady=10)
    sender_entry = tk.Entry(main_window)
    sender_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(main_window, text="Nama Penerima:").grid(row=1, column=0, padx=10, pady=10)
    receiver_entry = tk.Entry(main_window)
    receiver_entry.grid(row=1, column=1, padx=10, pady=10)
    
    tk.Label(main_window, text="Kota Tujuan:").grid(row=2, column=0, padx=10, pady=10)
    city_entry = tk.Entry(main_window)
    city_entry.grid(row=2, column=1, padx=10, pady=10)
    
    tk.Label(main_window, text="Berat Paket (kg):").grid(row=3, column=0, padx=10, pady=10)
    weight_entry = tk.Entry(main_window)
    weight_entry.grid(row=3, column=1, padx=10, pady=10)
    
    tk.Button(main_window, text="Hitung Biaya", command=calculate_cost).grid(row=4, column=0, columnspan=2, pady=10)
    
    main_window.mainloop()

# Fungsi untuk menghitung biaya pengiriman
def calculate_cost():
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    city = city_entry.get()
    weight = weight_entry.get()
    
    if not sender or not receiver or not city or not weight:
        messagebox.showerror("Error", "Semua kolom harus diisi!")
        return
    
    try:
        weight = float(weight)
    except ValueError:
        messagebox.showerror("Error", "Berat harus berupa angka!")
        return
    
    if city not in data["distance_prices"]:
        messagebox.showerror("Error", f"Kota {city} tidak tersedia!")
        return
    
    base_cost = weight * 10000
    distance_cost = data["distance_prices"][city]
    total_cost = base_cost + distance_cost
    
    result = (
        f"Nama Pengirim: {sender}\n"
        f"Nama Penerima: {receiver}\n"
        f"Kota Tujuan: {city}\n"
        f"Berat Paket: {weight} kg\n"
        f"Biaya Dasar: Rp {base_cost:,}\n"
        f"Biaya Jarak: Rp {distance_cost:,}\n"
        f"Total Biaya: Rp {total_cost:,}\n"
    )
    messagebox.showinfo("Rincian Biaya", result)

# Menjalankan program
if __name__ == "__main__":
    data = load_data()
    if data is not None:
        root = tk.Tk()
        root.title("Login Pengiriman Paket")
        
        tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(root)
        username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(root, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(root, text="Login", command=login).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(root, text="Register", command=show_register_window).grid(row=2, column=1, padx=10, pady=10)
        
        root.mainloop()


