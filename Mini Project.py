print("=========================================================")
print("Analisis Ketersediaan Tempat Tidur Rumah Sakit           ")
print("       pada Setiap Provinsi di Indonesia                 ")
print("=========================================================")

import csv
import statistics

nama_file = "data/rumah_sakit_per_provinsi_2023_2024.csv"
file_akun = "akun.csv"
kolom_angka = ["RS 2023", "TT Jumlah 2023", "TT Rasio 2023", "RS 2024", "TT Jumlah 2024", "TT Rasio 2024"]
kolom_wajib = ["Provinsi"] + kolom_angka
data_valid = []

def validasi_input(baris):
    provinsi = (baris.get("Provinsi") or "").strip()
    if not provinsi:
        return False, "Nama provinsi kosong."
    bersih = {"prov": provinsi}
    for kolom in kolom_angka:
        teks = (baris.get(kolom) or "").strip()
        if kolom == "TT Rasio 2023" and not teks:
            bersih[kolom] = None
            continue
        if not teks:
            return False, f"Data {kolom} kosong."
        try:
            nilai = float(teks)
        except (ValueError, TypeError):
            return False, f"Data {kolom} bukan angka."
        if nilai != nilai or nilai in (float("inf"), float("-inf")) or nilai < 0:
            return False, f"Data {kolom} tidak valid atau negatif."
        if kolom in ("RS 2023", "TT Jumlah 2023", "RS 2024", "TT Jumlah 2024") and not nilai.is_integer():
            return False, f"Data {kolom} harus bilangan bulat."
        bersih[kolom] = nilai
    return True, bersih

def format_angka(nilai, digit=0):
    teks = f"{nilai:,.{digit}f}"
    return teks.replace(",", "X").replace(".", ",").replace("X", ".")

def kategori(rasio):
    if rasio >= 2:
        return "Ideal"
    elif rasio >= 1:
        return "Cukup"
    return "Kurang"

def perubahan(baru, lama):
    selisih = baru - lama
    if selisih > 0:
        return f"naik {format_angka(selisih)}"
    elif selisih < 0:
        return f"turun {format_angka(abs(selisih))}"
    return "tetap"

def pilih_tahun():
    while True:
        print("PILIH TAHUN")
        print("1. 2023")
        print("2. 2024")
        print("0. Kembali")
        pilihan = input("Pilih tahun: ").strip()
        if pilihan in ("1", "2"):
            return "2023" if pilihan == "1" else "2024"
        if pilihan == "0":
            return None
        print("Pilihan tahun tidak valid.")

def akun_tersimpan():
    try:
        with open(file_akun, "r", encoding="utf-8", newline="") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []

def registrasi():
    print("REGISTRASI")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if not username or not password:
        print("Username dan password tidak boleh kosong.")
        return
    akun = akun_tersimpan()
    for data in akun:
        if data["username"].lower() == username.lower():
            print("Username sudah terdaftar. Gunakan username lain.")
            return
    with open(file_akun, "a", encoding="utf-8", newline="") as file:
        penulis = csv.writer(file)
        if not akun:
            penulis.writerow(["username", "password"])
        penulis.writerow([username, password])
    print("Registrasi berhasil. Silakan login (menu 2).")

def login():
    print("LOGIN")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    for akun in akun_tersimpan():
        if akun["username"] == username and akun["password"] == password:
            print(f"Login berhasil. Selamat datang, {username}!")
            return username
    print("Username atau password tidak sesuai.")
    return None

def jawaban(pesan):
    while True:
        hasil = input(pesan).strip().lower()
        if hasil in ("ya", "tidak", "batal"):
            return hasil
        print("Input tidak valid. Masukkan ya atau tidak.")

def menu_konsultasi(nama_pengguna):
    if not data_valid:
        print("Tidak ada data valid untuk konsultasi.")
        return
    print(f"Halo, {nama_pengguna}. Konsultasi ketersediaan tempat tidur rumah sakit.")
    print("Ketik 'batal' untuk kembali ke menu.")
    butuh = jawaban("Apakah Anda atau keluarga membutuhkan perawatan rumah sakit? (ya/tidak): ")
    if butuh != "ya":
        print("Konsultasi dibatalkan.")
        return
    while True:
        darurat = jawaban("Apakah pasien dalam kondisi darurat dan perlu rawat inap segera? (ya/tidak): ")
        if darurat == "batal":
            return
        if darurat == "ya":
            print("Untuk kondisi darurat, segera hubungi IGD atau layanan darurat setempat.")
        while True:
            kata = input("Provinsi mana yang ingin dicek (contoh: Aceh, Jawa Barat, Papua): ").strip()
            if kata.lower() == "batal":
                return
            hasil = [d for d in data_valid if kata.lower() in d["prov"].lower()]
            if len(hasil) == 1:
                provinsi = hasil[0]
                break
            if hasil:
                print("Ditemukan beberapa provinsi yang sesuai:")
                print(", ".join(d["prov"] for d in hasil))
                print("Masukkan nama provinsi yang lebih lengkap.")
            else:
                print("Provinsi tidak ditemukan. Periksa kembali nama provinsi.")
        rasio, lama = provinsi["TT Rasio 2024"], provinsi["TT Rasio 2023"]
        peringkat = 1 + sum(d["TT Rasio 2024"] > rasio for d in data_valid)
        print()
        print(f"INFORMASI TEMPAT TIDUR RS: {provinsi['prov'].upper()}")
        print(f"Jumlah RS 2024            : {format_angka(provinsi['RS 2024'])} ({perubahan(provinsi['RS 2024'], provinsi['RS 2023'])} dari 2023)")
        print(f"Jumlah tempat tidur 2024  : {format_angka(provinsi['TT Jumlah 2024'])} ({perubahan(provinsi['TT Jumlah 2024'], provinsi['TT Jumlah 2023'])} dari 2023)")
        print(f"Rasio per 1.000 penduduk  : {format_angka(rasio, 1)} ({kategori(rasio)})")
        print(f"Peringkat rasio nasional  : {peringkat} dari {len(data_valid)} provinsi")
        if darurat == "ya":
            kesimpulan = "Kondisi darurat perlu segera ditangani di IGD."
        elif rasio < 1:
            kesimpulan = f"Tidak sesuai. Rasio {format_angka(rasio, 1)} berada di bawah batas 1,0."
        elif lama is not None and rasio < lama:
            kesimpulan = f"Sesuai berdasarkan batas rasio, tetapi turun dari {format_angka(lama, 1)} menjadi {format_angka(rasio, 1)}."
        else:
            kesimpulan = f"Sesuai. Pasien tidak dalam kondisi darurat dan rasio {format_angka(rasio, 1)} berada di atas batas 1,0."
        print(f"Kesimpulan                : {kesimpulan}")
        if jawaban("Apakah ingin memeriksa provinsi lain? (ya/tidak): ") != "ya":
            print("Konsultasi selesai.")
            return

def ringkasan_statistik(data, tahun):
    rs, tt, rasio = f"RS {tahun}", f"TT Jumlah {tahun}", f"TT Rasio {tahun}"
    tersedia = [d[rasio] for d in data if d[rasio] is not None]
    print(f"RINGKASAN STATISTIK {tahun}")
    print(f"Jumlah provinsi      : {len(data)}")
    print(f"Total rumah sakit    : {format_angka(sum(d[rs] for d in data))}")
    print(f"Total tempat tidur   : {format_angka(sum(d[tt] for d in data))}")
    if not tersedia:
        print("Rata-rata rasio      : Tidak tersedia")
        print("Rasio tertinggi      : Tidak tersedia")
        print("Rasio terendah       : Tidak tersedia")
        return
    atas, bawah = max(tersedia), min(tersedia)
    nama_atas = [d["prov"] for d in data if d[rasio] == atas]
    nama_bawah = [d["prov"] for d in data if d[rasio] == bawah]
    print(f"Rata-rata rasio      : {format_angka(statistics.mean(tersedia), 2)}")
    print(f"Rasio tertinggi      : {', '.join(nama_atas)} ({format_angka(atas, 2)})")
    print(f"Rasio terendah       : {', '.join(nama_bawah)} ({format_angka(bawah, 2)})")

def menu_klasifikasi():
    tahun = pilih_tahun()
    if tahun is None:
        return
    while True:
        print("KLASIFIKASI RASIO")
        print("1. Ideal")
        print("2. Cukup")
        print("3. Kurang")
        print("4. Semua")
        print("0. Kembali")
        pilihan = input("Pilih kategori: ").strip()
        if pilihan == "0":
            continue
        if pilihan in ("1", "2", "3", "4"):
            print("Fitur klasifikasi dilengkapi pada Commit 7.")
        else:
            print("Pilihan tidak valid.")

daftar_invalid = []
try:
    with open(nama_file, "r", encoding="utf-8-sig", newline="") as file:
        pembaca = csv.DictReader(file)
        if not pembaca.fieldnames:
            print("File CSV tidak memiliki header.")
            raise SystemExit
        hilang = [k for k in kolom_wajib if k not in pembaca.fieldnames]
        if hilang:
            print("Kolom tidak ditemukan: " + ", ".join(hilang))
            raise SystemExit
        for baris in pembaca:
            valid, hasil = validasi_input(baris)
            if valid:
                data_valid.append(hasil)
            else:
                daftar_invalid.append((pembaca.line_num, hasil))
except FileNotFoundError:
    print("File CSV tidak ditemukan.")
    raise SystemExit
except OSError:
    print("File CSV tidak dapat dibaca.")
    raise SystemExit

print(f"Data dibaca: {len(data_valid)} valid, {len(daftar_invalid)} ditolak.")
if daftar_invalid:
    print("PEMERIKSAAN DATASET")
    for nomor, alasan in daftar_invalid:
        print(f"Baris {nomor}: {alasan}")
elif data_valid:
    print("Tidak ada data yang ditolak saat validasi.")
else:
    print("Dataset tidak memiliki baris data.")

pengguna = None
while True:
    print("\nMENU UTAMA")
    print("1. Registrasi")
    print("2. Login")
    print("3. Konsultasi Tempat Tidur")
    print("4. Jumlah RS & Tempat Tidur")
    print("5. Klasifikasi Rasio")
    print("6. Ringkasan & Perubahan 2023-2024")
    print("7. Keluar")
    pilihan = input("Pilih menu: ").strip()
    if pilihan == "1":
        registrasi()
    elif pilihan == "2":
        pengguna = login()
    elif pilihan in ("3", "4", "5", "6") and not pengguna:
        print("Silakan login dahulu (menu 2).")
    elif pilihan == "3":
        menu_konsultasi(pengguna)
    elif pilihan == "4":
        print("Menu jumlah RS dan tempat tidur diselesaikan pada Commit 7.")
    elif pilihan == "5":
        menu_klasifikasi()
    elif pilihan == "6":
        tahun = pilih_tahun()
        if tahun:
            ringkasan_statistik(data_valid, tahun)
    elif pilihan == "7":
        print("Terima kasih. Program selesai.")
        break
    else:
        print("Pilihan tidak valid. Masukkan angka 1 sampai 7.")
