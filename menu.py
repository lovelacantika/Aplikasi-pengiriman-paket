import tkinter as tk
from tkinter import PhotoImage
from paket import main_window

def main_menu():
    """Menampilkan menu utama."""
    menu_window = tk.Tk()
    menu_window.geometry("700x700")
    menu_window.title("Menu Utama")
    
    background_image = PhotoImage(file= "opening,png.png" )  # Ganti dengan path file gambar Anda
    canvas = tk.Canvas(menu_window, width=700, height=700)
    canvas.pack(fill="both", expand=True)

    # Menambahkan gambar ke Canvas
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Menambahkan tombol dengan posisi yang diatur di atas canvas
    canvas.create_window(350, 200, window=tk.Button(menu_window, text="Kirim Paket", command=main_window, font=("Arial", 16)))
    canvas.create_window(350, 300, window=tk.Button(menu_window, text="Cek Riwayat", command=main_window, font=("Arial", 16)))
    canvas.create_window(350, 400, window=tk.Button(menu_window, text="Keluar", command=menu_window.destroy, font=("Arial", 16)))

    menu_window.mainloop()
    
