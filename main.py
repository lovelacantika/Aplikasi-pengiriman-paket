import tkinter as tk
from auth import login, register
from PIL import Image, ImageTk
from tkinter import messagebox
from menu import main_menu

# Fungsi untuk mencoba login
def attempt_login(username_entry, password_entry, root):
    username = username_entry.get()
    password = password_entry.get()
    if login(username, password, root):  # Fungsi `login` dari `auth`
        root.destroy()
        main_menu()  # Panggil menu utama setelah login berhasil
    else:
        messagebox.showerror("Error", "Login gagal!")  # Pesan error jika login gagal

# Fungsi untuk menampilkan jendela registrasi
def show_register_window(root):
    root.destroy()  # Tutup jendela login
    create_register_window()  # Panggil jendela registrasi

# Fungsi untuk membuat jendela login
def create_login_window():
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title("Login Pengiriman Paket")

    # Memuat gambar latar belakang dan mengubah ukurannya
    original_image = Image.open("login.png")  # Ganti dengan path file gambar Anda
    resized_image = original_image.resize((1300, 700))  # Sesuaikan ukuran dengan jendela
    background_image = ImageTk.PhotoImage(resized_image)

    # Membuat Canvas dan menambahkan gambar
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Menambahkan elemen GUI di atas canvas
    username_label = tk.Label(root, text="Username:", font=("Arial", 16), bg="white")
    username_entry = tk.Entry(root, font=("Arial", 16))
    password_label = tk.Label(root, text="Password:", font=("Arial", 16), bg="white")
    password_entry = tk.Entry(root, font=("Arial", 16), show="*")

    # Tombol Login dan Register
    login_button = tk.Button(root, text="Login", 
                             command=lambda: attempt_login(username_entry, password_entry, root), 
                             font=("Arial", 16))
    register_button = tk.Button(root, text="Register", 
                                command=lambda: show_register_window(root), 
                                font=("Arial", 16))

    # Menempatkan elemen menggunakan canvas.create_window
    canvas.create_window(130, 125, anchor="nw", window=username_label)
    canvas.create_window(300, 125, anchor="nw", window=username_entry)
    canvas.create_window(130, 200, anchor="nw", window=password_label)
    canvas.create_window(300, 200, anchor="nw", window=password_entry)
    canvas.create_window(150, 300, anchor="nw", window=login_button)
    canvas.create_window(410, 300, anchor="nw", window=register_button)

    root.mainloop()
    
def register_user(username_entry, password_entry, reg_window):
    username = username_entry.get()  # Ambil input dari entry
    password = password_entry.get()  # Ambil input dari entry
    if register(username, password):  # Fungsi `register` dari `auth`
        messagebox.showinfo("Sukses", "Registrasi berhasil!")
        reg_window.destroy()
        main_menu()
    else:
        messagebox.showerror("Error", "Username sudah digunakan atau input tidak valid!")
        
# Fungsi untuk membuat jendela registrasi
def create_register_window():
    reg_window = tk.Tk()
    reg_window.geometry("1920x1080")
    reg_window.title("Registrasi")

    # Memuat gambar latar belakang dan mengubah ukurannya
    original_image = Image.open("optionkota.png")  # Ganti dengan path file gambar Anda
    resized_image = original_image.resize((1300, 700))  # Sesuaikan ukuran dengan jendela
    background_image = ImageTk.PhotoImage(resized_image)

    # Membuat Canvas dan menambahkan gambar
    canvas = tk.Canvas(reg_window, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Menambahkan elemen GUI di atas canvas
    reg_username_label = tk.Label(reg_window, text="Username:", font=("Arial", 16), bg="white")
    reg_username_entry = tk.Entry(reg_window, font=("Arial", 16))
    reg_password_label = tk.Label(reg_window, text="Password:", font=("Arial", 16), bg="white")
    reg_password_entry = tk.Entry(reg_window, font=("Arial", 16), show="*")

    register_button = tk.Button(reg_window, text="Register",command=lambda: register_user(reg_username_entry, reg_password_entry, reg_window), 
                            font=("Arial", 16))

    canvas.create_window(130, 125, anchor="nw", window=reg_username_label)
    canvas.create_window(300, 125, anchor="nw", window=reg_username_entry)
    canvas.create_window(130, 200, anchor="nw", window=reg_password_label)
    canvas.create_window(300, 200, anchor="nw", window=reg_password_entry)
    canvas.create_window(410, 300, anchor="nw", window=register_button)

    reg_window.mainloop()

# Memulai aplikasi hanya jika dijalankan langsung
if __name__ == "__main__":
    create_login_window()  # Mulai aplikasi dengan jendela login
