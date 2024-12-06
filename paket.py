import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from utils import load_json

def calculate_cost():
    """Menghitung biaya pengiriman berdasarkan input."""
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    province = province_combobox.get()
    city_selected = city_combobox.get()
    weight = weight_entry.get()
    shipment_date = date_entry.get()

    # Validasi Input
    if not sender or not receiver or not province or not city_selected or not weight or not shipment_date:
        messagebox.showerror("Error", "Semua kolom harus diisi!")
        return

    try:
        weight = float(weight)
    except ValueError:
        messagebox.showerror("Error", "Berat harus berupa angka!")
        return

    # Load Data Harga dari JSON
    data_harga = load_json("data/harga.json")
    if not data_harga:
        return

    if province not in data_harga or city_selected not in data_harga[province]:
        messagebox.showerror("Error", f"Kota {city_selected} tidak tersedia!")
        return

    # Perhitungan Biaya
    base_cost = weight * 10000
    distance_cost = data_harga[province][city_selected][0]
    total_cost = base_cost + distance_cost
    estimasi_waktu = data_harga[province][city_selected][1]

    # Hitung Tanggal Pengiriman
    try:
        shipment_datetime = datetime.strptime(shipment_date, "%d-%m-%Y")
        delivery_datetime = shipment_datetime + timedelta(days=estimasi_waktu)
        delivery_date = delivery_datetime.strftime("%A, %d %B %Y")
    except ValueError:
        messagebox.showerror("Error", "Format tanggal pengiriman salah!")
        return

    # Format Hasil
    result = (
        f"Nama Pengirim     : {sender}\n"
        f"Nama Penerima     : {receiver}\n"
        f"Tanggal Pengiriman: {shipment_date}\n"
        f"Kota Tujuan       : {city_selected}\n"
        f"Berat Paket       : {weight} kg\n"
        f"Biaya Dasar       : Rp {base_cost}\n"
        f"Biaya Jarak       : Rp {distance_cost}\n"
        f"Total Biaya       : Rp {total_cost}\n"
        f"Estimasi Sampai   : {delivery_date}"
    )

    # Simpan ke File TXT
    try:
        file_name = f"nota_pengiriman_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(file_name, "w") as file:
            file.write("NOTA PENGIRIMAN\n")
            file.write("=" * 50 + "\n")
            file.write(result + "\n")
            file.write("=" * 50 + "\n")
        messagebox.showinfo("Sukses", f"Nota berhasil disimpan sebagai {file_name}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan nota: {e}")
        return

    # Tampilkan Hasil di Jendela
    messagebox.showinfo("Hasil Perhitungan", result)


def main_window():
    """Menampilkan jendela input pengiriman paket."""
    global sender_entry, receiver_entry, province_combobox, city_combobox, weight_entry, date_entry
    main_window = tk.Tk()
    main_window.geometry("700x700")
    main_window.title("Pengiriman Paket")

    # Form input
    tk.Label(main_window, text="Nama Pengirim:", font=("Arial", 20)).place(x=75, y=50)
    sender_entry = tk.Entry(main_window, font=("Arial", 20))
    sender_entry.place(x=300, y=50)
    tk.Label(main_window, text="Nama Penerima:", font=("Arial", 20)).place(x=75, y=150)
    receiver_entry = tk.Entry(main_window, font=("Arial", 20))
    receiver_entry.place(x=300, y=150)

    # Dropdown Provinsi
    tk.Label(main_window, text="Provinsi Tujuan:", font=("Arial", 20)).place(x=75, y=250)
    province_combobox = ttk.Combobox(main_window, values=provinces, state="readonly", font=("Arial", 15))
    province_combobox.place(x=300, y=250)
    province_combobox.bind("<<ComboboxSelected>>", update_city)

    # Dropdown Kota
    tk.Label(main_window, text="Kota Tujuan:", font=("Arial", 20)).place(x=75, y=350)
    city_combobox = ttk.Combobox(main_window, values=[], state="readonly", font=("Arial", 15))
    city_combobox.place(x=300, y=350)

    # Input Berat Paket
    tk.Label(main_window, text="Berat Paket (kg):", font=("Arial", 20)).place(x=75, y=450)
    weight_entry = tk.Entry(main_window, font=("Arial", 20))
    weight_entry.place(x=300, y=450)

    # Input Tanggal Pengiriman
    tk.Label(main_window, text="Tanggal Pengiriman:", font=("Arial", 20)).place(x=75, y=550)
    date_entry = DateEntry(main_window, width=18, background="darkblue", foreground="white", font=("Arial", 15), date_pattern="dd-mm-yyyy")
    date_entry.place(x=300, y=550)

    # Tambahan form lainnya...

    tk.Button(main_window, text="Hitung Biaya", command=calculate_cost, font=("Arial", 15)).place(x=280, y=630)
    main_window.mainloop()
    
def update_city(event):
    selected_province = province_combobox.get()
    city_combobox["values"] = city.get(selected_province, [])
    city_combobox.set("")
provinces = ["Jawa Barat", "Jawa Tengah", "Jawa Timur", "DKI Jakarta", "Banten"]
city = {
    "Jawa Barat": ["Bandung", "Bogor", "Bekasi", "Depok", "Cirebon"],
    "Jawa Tengah": ["Semarang", "Magelang", "Kudus", "Pati", "Pekalongan"],
    "Jawa Timur": ["Surabaya", "Malang", "Kediri", "Blitar", "Madiun"],
    "DKI Jakarta": ["Jakarta Pusat", "Jakarta Timur", "Jakarta Barat", "Jakarta Selatan", "Jakarta Utara"],
    "Banten": ["Serang", "Tangerang", "Cilegon", "Lebak", "Pandeglang"]
}