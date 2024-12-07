import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from utils import load_json,load_harga
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        print("Koneksi ke server berhasil!")
except Exception as e:
    print(f"Error koneksi: {e}")
    
def calculate_cost():
    hasil= tk.Toplevel()
    hasil.geometry("400x400")
    """Menghitung biaya pengiriman berdasarkan input."""
    sender = sender_entry.get()
    receiver= receiver_entry.get()
    email_sender = email_entry.get()
    province = province_combobox.get()
    city_selected = city_combobox.get()
    weight = weight_entry.get()
    shipment_date = date_entry.get()
    data_harga = load_json("data/harga.json")
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
        delivery_datetime = shipment_datetime + timedelta(days=int(estimasi_waktu))
        delivery_date = delivery_datetime.strftime("%A, %d %B %Y")
    except ValueError:
        messagebox.showerror("Error", "Format tanggal pengiriman salah!")
        return

    # Format Hasil
    result = (
        f"Nama Pengirim     : {sender}\n"
        f"Nama Penerima     : {receiver}\n"
        f"Email             : {email_sender}\n"
        f"Tanggal Pengiriman: {shipment_date}\n"
        f"Tujuan            : {city_selected}, {province}\n"
        f"Berat Paket       : {weight} kg\n"
        f"Biaya Dasar       : Rp {base_cost}\n"
        f"Biaya Jarak       : Rp {distance_cost}\n"
        f"Total Biaya       : Rp {total_cost}\n"
        f"Estimasi Sampai   : {delivery_date}"
    )
    tk.Label(hasil, text= result, font=("Arial", 12)).pack(pady=10)
    
    # Contoh penggunaan
    email_terima = email_sender  # Ganti dengan email penerima yang diinput
    email_sent = send_invoice_email(
    sender, receiver, city_selected ,weight, shipment_date, delivery_date, total_cost, email_terima)
    if email_sent:
       messagebox.showinfo("Sukses", "Invoice berhasil dikirim ke email!")
    else:
       messagebox.showerror("Error", "Gagal mengirim invoice ke email!")

    
    
    

def main_window():
    """Menampilkan jendela input pengiriman paket."""
    global sender_entry, receiver_entry,email_entry, province_combobox, city_combobox, weight_entry, date_entry
    main_window = tk.Tk()
    main_window.geometry("600x700")
    main_window.title("Pengiriman Paket")

    # Form input
    tk.Label(main_window, text="Nama Pengirim:", font=("Arial", 16)).place(x=75, y=50)
    sender_entry = tk.Entry(main_window, font=("Arial", 16))
    sender_entry.place(x=300, y=50)
    tk.Label(main_window, text="Nama Penerima:", font=("Arial", 16)).place(x=75, y=150)
    receiver_entry = tk.Entry(main_window, font=("Arial", 16))
    receiver_entry.place(x=300, y=150)
    tk.Label(main_window, text="email:", font=("Arial", 16)).place(x=75, y=200)
    email_entry = tk.Entry(main_window, font=("Arial", 16))
    email_entry.place(x=300, y=200)
    # Dropdown Provinsi
    tk.Label(main_window, text="Provinsi Tujuan:", font=("Arial", 16)).place(x=75, y=250)
    province_combobox = ttk.Combobox(main_window, values=provinces, state="readonly", font=("Arial", 15))
    province_combobox.place(x=300, y=250)
    province_combobox.bind("<<ComboboxSelected>>", update_city)

    # Dropdown Kota
    tk.Label(main_window, text="Kota Tujuan:", font=("Arial", 16)).place(x=75, y=350)
    city_combobox = ttk.Combobox(main_window, values=[], state="readonly", font=("Arial", 15))
    city_combobox.place(x=300, y=350)

    # Input Berat Paket
    tk.Label(main_window, text="Berat Paket (kg):", font=("Arial", 16)).place(x=75, y=450)
    weight_entry = tk.Entry(main_window, font=("Arial", 16))
    weight_entry.place(x=300, y=450)

    # Input Tanggal Pengiriman
    tk.Label(main_window, text="Tanggal Pengiriman:", font=("Arial", 16)).place(x=75, y=550)
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

def send_invoice_email(sender, receiver, city, weight, shipment_date, delivery_date, total_cost, email):
    try:
        sender_email = "bhalosanypakett@gmail.com"  # Ganti dengan email pengirim
        sender_password = "giuj umzl jgzn fcih"  # Ganti dengan password email pengirim
        subject = "Invoice Pengiriman Paket"
        
        body = f"""
        <html>
        <body>
            <h2>Invoice Pengiriman Paket</h2>
            <p><strong>Pengirim:</strong> {sender}</p>
            <p><strong>Penerima:</strong> {receiver}</p>
            <p><strong>Kota Tujuan:</strong> {city}</p>
            <p><strong>Berat:</strong> {weight} kg</p>
            <p><strong>Tanggal Pengiriman:</strong> {shipment_date}</p>
            <p><strong>Estimasi Sampai:</strong> {delivery_date}</p>
            <p><strong>Total Biaya:</strong> Rp {total_cost:,}</p>
        </body>
        </html>
        """

        # Setup MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))

        # Connect to server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        
        print("Email berhasil dikirim!")
        return True
    except smtplib.SMTPAuthenticationError:
        print("Error: Autentikasi gagal. Periksa email dan kata sandi.")
    except smtplib.SMTPException as e:
        print(f"Error pengiriman email: {e}")
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
    
    return False
