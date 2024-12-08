import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from auth import load_json
from PIL import Image, ImageTk
import thanks as ths
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        print("Koneksi ke server berhasil!")
except Exception as e:
    print(f"Error koneksi: {e}")
    
def calculate_cost(main_window):
    def to_thanks():
        hasil.destroy()
        ths.thanks_page()
    hasil= tk.Tk()
    hasil.geometry("1920x1080")
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
    tk.Label(hasil, text= result, font=("Arial", 12)).place(y=200, x=300)
    
    # Contoh penggunaan
    email_terima = email_sender  # Ganti dengan email penerima yang diinput
    email_sent = send_invoice_email(
    sender, receiver, city_selected ,weight, shipment_date, delivery_date, total_cost, email_terima)
    if email_sent:
       messagebox.showinfo("Sukses", "Invoice berhasil dikirim ke email!")
       main_window.destroy()
    else:
       messagebox.showerror("Error", "Gagal mengirim invoice ke email!")

    tk.Button(hasil, text="Hitung Biaya", command=to_thanks, font=("Arial", 15)).place(y=500, x=300)
    hasil.mainloop()


def main_window():
    def hitung_biaya():
        main_window.withdraw()
        calculate_cost(main_window)

    """Menampilkan jendela input pengiriman paket."""
    global sender_entry, receiver_entry,email_entry, province_combobox, city_combobox, weight_entry, date_entry
    main_window = tk.Tk()
    main_window.geometry("940x1080")
    main_window.title("Pengiriman Paket")
    resi_image = Image.open("resi.png.png")  # Ganti dengan path file gambar Anda
    resized_resi = resi_image.resize((1300, 700))  # Sesuaikan ukuran dengan jendela
    background_image = ImageTk.PhotoImage(resized_resi)
    canvas = tk.Canvas(main_window, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Form input
    tk.Label(main_window, text="Nama Pengirim:", font=("Arial", 16)).place(x=75, y=50)
    sender_entry = tk.Entry(main_window, font=("Arial", 16))
    sender_entry.place(x=300, y=50)
    tk.Label(main_window, text="Nama Penerima:", font=("Arial", 16)).place(x=75, y=100)
    receiver_entry = tk.Entry(main_window, font=("Arial", 16))
    receiver_entry.place(x=300, y=100)
    tk.Label(main_window, text="email:", font=("Arial", 16)).place(x=75, y=150)
    email_entry = tk.Entry(main_window, font=("Arial", 16))
    email_entry.place(x=300, y=150)
    # Dropdown Provinsi
    tk.Label(main_window, text="Provinsi Tujuan:", font=("Arial", 16)).place(x=75, y=200)
    province_combobox = ttk.Combobox(main_window, values=provinces, state="readonly", font=("Arial", 15))
    province_combobox.place(x=300, y=200)
    province_combobox.bind("<<ComboboxSelected>>", update_city)

    # Dropdown Kota
    tk.Label(main_window, text="Kota Tujuan:", font=("Arial", 16)).place(x=75, y=250)
    city_combobox = ttk.Combobox(main_window, values=[], state="readonly", font=("Arial", 15))
    city_combobox.place(x=300, y=250)

    # Input Berat Paket
    tk.Label(main_window, text="Berat Paket (kg):", font=("Arial", 16)).place(x=75, y=300)
    weight_entry = tk.Entry(main_window, font=("Arial", 16))
    weight_entry.place(x=300, y=300)

    # Input Tanggal Pengiriman
    tk.Label(main_window, text="Tanggal Pengiriman:", font=("Arial", 16)).place(x=75, y=350)
    date_entry = DateEntry(main_window, width=18, background="darkblue", foreground="white", font=("Arial", 15), date_pattern="dd-mm-yyyy")
    date_entry.place(x=300, y=350)

    # Tambahan form lainnya...

    tk.Button(main_window, text="Hitung Biaya", command=hitung_biaya, font=("Arial", 15)).place(x=200, y=500)
    main_window.mainloop()
    
def update_city(event):
    selected_province = province_combobox.get()
    city_combobox["values"] = city.get(selected_province, [])
    city_combobox.set("")
provinces = ["Jawa Barat", "Jawa Tengah", "Jawa Timur", "DKI Jakarta", "Banten"]
city = {
    "Jawa Barat": ["Bandung", "Bogor", "Bekasi", "Depok", "Cirebon","Tasikmalaya","Cimahi","Sumedang"],
    "Jawa Tengah": ["Semarang", "Magelang", "Kudus", "Pati", "Pekalongan","Demak","Jepara","Salatiga","Karanganyar","Sragen","Sukoharjo"],
    "Jawa Timur": ["Surabaya", "Malang","Batu","Probolinggo","Kediri", "Blitar", "Madiun"],
    "DKI Jakarta": ["Jakarta Pusat", "Jakarta Timur", "Jakarta Barat", "Jakarta Selatan", "Jakarta Utara"],
    "Banten": ["Serang", "Tangerang", "Cilegon", "Lebak", "Pandeglang"],
    "D.I.Yogyakarta": ["Yogyakarta"] 
    }

def send_invoice_email(sender, receiver, city, weight, shipment_date, delivery_date, total_cost, email):
    try:
        sender_email = "bhalosanypakett@gmail.com"  # Ganti dengan email pengirim
        sender_password = "giuj umzl jgzn fcih"  # Ganti dengan password email pengirim
        subject = "Invoice Pengiriman Paket"
        
        body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="border: 2px solid #FF69B4; border-radius: 10px; padding: 20px; max-width: 600px; margin: auto;">
        <h2 style="text-align: center; color: #4CAF50;">Invoice Pengiriman Paket</h2>
        <hr style="border: 1px solid #ddd;">
        <p><strong>Pengirim:</strong> {sender}</p>
        <p><strong>Penerima:</strong> {receiver}</p>
        <p><strong>Kota Tujuan:</strong> {city}</p>
        <p><strong>Berat:</strong> {weight} kg</p>
        <p><strong>Tanggal Pengiriman:</strong> {shipment_date}</p>
        <p><strong>Estimasi Sampai:</strong> {delivery_date}</p>
        <p><strong>Total Biaya:</strong> <span style="color: #4CAF50;">Rp {total_cost:,}</span></p>
        <hr style="border: 1px solid #ddd;">
        <p style="text-align: center; font-style: italic;">Terima kasih telah menggunakan layanan kami!</p>
    </div>
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
