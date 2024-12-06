import tkinter as tk
from paket import main_window

def main_menu():
    """Menampilkan menu utama."""
    menu_window = tk.Tk()
    menu_window.geometry("700x700")
    menu_window.title("Menu Utama")

    tk.Button(menu_window, text="Kirim Paket", command=main_window, font=("Arial", 16)).place(relx=0.5, rely=0.3, anchor="center")
    tk.Button(menu_window, text="Keluar", command=menu_window.destroy, font=("Arial", 16)).place(relx=0.5, rely=0.4, anchor="center")

    menu_window.mainloop()
