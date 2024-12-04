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

def load_harga():
    try:
        with open("harga.json", "r") as file:
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
    reg_window.geometry("700x700")
    reg_window.title("Registrasi")
    
    
    tk.Label(reg_window,text="Username:", font=("Arial", 20)).place(x= 130, y= 125)
    reg_username_entry = tk.Entry(reg_window, show="*",font=("Arial", 20))
    reg_username_entry.place(x= 300, y= 125)
    
    tk.Label(reg_window, text="Password:",font=("Arial", 20)).place(x= 130, y= 270)
    reg_password_entry = tk.Entry(reg_window, show="*",font=("Arial", 20))
    reg_password_entry.place(x= 300, y= 270)
    
    tk.Button(reg_window, text="Daftar", command=register, font=("Arial", 20)).place(x= 350, y= 375)
# Fungsi untuk menampilkan jendela utama
def show_main_window():
    global city_var
    global sender_entry, receiver_entry, city_entry, weight_entry
    main_window = tk.Tk()
    main_window.geometry("700x700")
    main_window.title("Pengiriman Paket")
    
    tk.Label(main_window, text="Nama Pengirim:",font=("Arial",20)).place(x=75,y=50)
    sender_entry = tk.Entry(main_window,font=("Arial",20))
    sender_entry.place(x= 300, y=50)
    
    
    tk.Label(main_window, text="Nama Penerima:",font=("Arial",20)).place(x= 75, y=200 )
    receiver_entry = tk.Entry(main_window,font=("Arial",20))
    receiver_entry.place(x= 300, y=200)



    city = [
        "Semarang", "Magelang", "Kudus", "Pati", "Pekalongan", "Klaten",
        "Salatiga", "Tegal", "Banjarnegara", "Purwokerto", "Boyolali",
        "Sragen", "Cilacap", "Kendal", "Demak", "Sukoharjo", "Brebes",
        "Blora", "Pemalang", "Rembang", "Jepara", "Wonosobo", "Temanggung", 
        "Karanganyar", "Kebumen", "Wonogiri", "Banyumas", "Purbalingga", 
        "Batang", "Purworejo", "Grobogan"
    ] 

    city_var = tk.StringVar(value="")
    tk.Label(main_window, text="Kota Tujuan:",font=("Arial",20)).place(x= 75, y=350)
    city_entry = tk.OptionMenu(main_window, city_var, *city)
    city_entry.config(font=("Arial", 15))
    city_entry.place(x= 300, y=350)
    
    tk.Label(main_window, text="Berat Paket (kg):",font=("Arial",20)).place(x= 75, y=500)
    weight_entry = tk.Entry(main_window,font=("Arial",20))
    weight_entry.place(x= 300, y=500)
    
    tk.Button(main_window, text="Hitung Biaya", command=calculate_cost,font=("Arial",15)).place(x=280,y=580)
    
    main_window.mainloop()

# Fungsi untuk menghitung biaya pengiriman
def calculate_cost():
    hasil = tk.Toplevel()
    hasil.geometry("400x400")
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    city = city_var.get()
    weight = weight_entry.get()
    data_harga = load_harga()
    
    if not sender or not receiver or not city or not weight:
        messagebox.showerror("Error", "Semua kolom harus diisi!")
        return
    
    try:
        weight = float(weight)
    except ValueError:
        messagebox.showerror("Error", "Berat harus berupa angka!")
        return

    # Validasi berat tidak boleh lebih dari 15 kg
    if weight > 15:
        messagebox.showerror("Error", "Berat tidak boleh lebih dari 15 kg!")
        return
    if city not in data_harga["distance_prices"][0].keys():
        messagebox.showerror("Error", f"Kota {city} tidak tersedia!")
        return
    
    base_cost = weight * 10000
    distance_cost = data_harga["distance_prices"][0][city][0]
    total_cost = base_cost + distance_cost

    # estimasi waktu
    estimasi_waktu = data_harga["distance_prices"][0][city][1]
    
    result = (
        f"Nama Pengirim     : {sender}\n"
        f"Nama Penerima     : {receiver}\n"
        f"Kota Tujuan       : {city}\n"
        f"Berat Paket       : {weight} kg\n"
        f"Biaya Dasar       : Rp {base_cost}\n"
        f"Biaya Jarak       : Rp {distance_cost}\n"
        f"Total Biaya       : Rp {total_cost}\n"
        f"Estimasi Sampai   : { estimasi_waktu}\n"
    )

    tk.Label(hasil, text=result, font=("Arial",20)).place(x= 60, y = 50)

    hasil.mainloop()

# Menjalankan program
if __name__ == "__main__":
    data = load_data()
    if data is not None:
        root = tk.Tk()
        root.geometry("700x500")
        root.title("Login Pengiriman Paket")
        
        tk.Label(root, text="Username:", font=("Arial", 20)).place(x= 130, y= 125)
        username_entry = tk.Entry(root,font=("Arial", 20))
        username_entry.place(x= 300, y= 125)
        
        tk.Label(root, text="Password:",font=("Arial", 20)).place(x= 130, y= 270)
        password_entry = tk.Entry(root,font=("Arial", 20))
        password_entry.place(x= 300, y= 270)
        
        tk.Button(root, text="Login", command=login,font=("Arial", 20)).place(x= 150, y= 375)
        tk.Button(root, text="Register", command=show_register_window,font=("Arial", 20)).place(x= 410, y= 375)
        root.mainloop()
