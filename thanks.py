import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk  # Untuk mengubah ukuran gambar

def thanks_page():
    def keluar():
        thanks_window.destroy()

    def resize_background(event):
        # Mengubah ukuran gambar sesuai ukuran jendela
        new_width = event.width
        new_height = event.height
        resized_image = original_image.resize((1300,700))  # Resize tanpa opsi anti-aliasing
        new_background = ImageTk.PhotoImage(resized_image)
        canvas.itemconfig(bg_image_id, image=new_background)
        canvas.image = new_background  # Menyimpan referensi agar tidak dihapus oleh garbage collector

    thanks_window = tk.Tk()
    thanks_window.geometry("1920x1080")
    thanks_window.title("Thank you")

    # Membaca gambar asli
    original_image = Image.open("closing.png.png")  # Ganti dengan path gambar Anda
    tk_original_image = ImageTk.PhotoImage(original_image)

    # Membuat canvas
    canvas = tk.Canvas(thanks_window, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)

    # Menambahkan gambar ke Canvas
    bg_image_id = canvas.create_image(0, 0, image=tk_original_image, anchor="nw")

    # Menambahkan tombol dengan posisi yang diatur di atas canvas
    canvas.create_window(350, 200, window=tk.Button(thanks_window, text="EXIT", command=keluar, font=("Arial", 16)))

    # Bind event resize untuk menyesuaikan ukuran gambar
    thanks_window.bind("<Configure>", resize_background)

    thanks_window.mainloop()


