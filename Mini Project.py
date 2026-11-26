judul1 = "Klasifikasi Tingkat Ketersediaan Tempat Tidur Rumah Sakit"
judul2 = "pada Setiap Provinsi di Indonesia Berbasis Python"
kelompok = "Kelompok 2C"
asisten = "Jihan Fitri Sakinah"
dosen = "Dr. Asmuliardi Muluk, S.T., M.T."
tahun = "2026"

LEBAR = 90  # lebar kertas 

def baris(teks=""):
    # mencetak 1 baris di tengah, dengan garis | di kiri dan kanan
    print("|" + teks.center(LEBAR) + "|")

print("+" + "-" * LEBAR + "+")   # garis atas

baris()
baris()
baris()
baris("MINI PROJECT")
baris()
baris("PEMROGRAMAN KOMPUTER")
baris()
baris("(" + judul1)
baris(judul2 + ")")
baris()
baris()

baris("Oleh :")
baris()
baris(kelompok)
baris()
baris()

baris("Anggota :")
baris()
baris("Syukra Hidayatullah      2610932010")
baris("Puti Andini              2610932046")
baris("Qodima Bisyarah          2610931003")
baris("Indah Fitriani           2610931011")
baris()
baris()
baris()

baris("Asisten Pembimbing :")
baris()
baris(asisten)
baris()
baris()
baris()

baris("Dosen Pengampu :")
baris()
baris(dosen)
baris()
baris()
baris()
baris()

baris("LABORATORIUM SISTEM INFORMASI DAN KEPUTUSAN")
baris()
baris("DEPARTEMEN TEKNIK INDUSTRI")
baris()
baris("FAKULTAS TEKNIK")
baris()
baris("UNIVERSITAS ANDALAS")
baris()
baris(tahun)
baris()
baris()
baris()

print("+" + "-" * LEBAR + "+") 

print("\n=========================================================")
print("Klasifikasi Tingkat Ketersediaan Tempat Tidur Rumah Sakit")
print("    pada Setiap Provinsi di Indonesia Berbasis Python    ")
print("=========================================================")
import csv
import statistics
FILE_DATA = "data/rumah_sakit_per_provinsi_2023_2024.csv"
FILE_AKUN = "akun.csv"
KOLOM = ["Estimasi Penduduk 2022", "RS 2023", "TT Jumlah 2023",
         "Estimasi Penduduk 2023", "RS 2024", "TT Jumlah 2024"]

def validasi_input(baris):
    provinsi = (baris.get("Provinsi") or "").strip()
    if not provinsi: return False, "Terdapat data yang kosong."
    bersih = {"prov": provinsi}
    for kolom in KOLOM + ["TT Rasio 2023", "TT Rasio 2024"]:
        teks = (baris.get(kolom) or "").strip()
        if kolom == "TT Rasio 2023" and not teks:
            bersih[kolom] = None
            continue
        if not teks: return False, "Terdapat data yang kosong."
        try: nilai = float(teks)
        except (ValueError, TypeError): return False, "Terdapat kesalahan pada data CSV."
        if nilai != nilai or nilai in (float("inf"), float("-inf")):
            return False, "Terdapat kesalahan pada data CSV."
        if nilai < 0: return False, "Terdapat data berupa angka negatif."
        if kolom in KOLOM and not nilai.is_integer():
            return False, "Terdapat kesalahan pada data CSV."
        bersih[kolom] = int(nilai) if kolom in KOLOM else nilai
    return True, bersih

def format_angka(nilai, digit=0):
    return f"{nilai:,.{digit}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def tabel(kepala, isi, rata=()):
    semua = [kepala] + isi
    lebar = [max(len(str(baris[i])) for baris in semua) for i in range(len(kepala))]
    garis = "-" * (sum(lebar) + 3 * len(lebar) + 1)
    print(garis)
    for baris in semua:
        teks = [str(baris[i]).rjust(lebar[i]) if i in rata else str(baris[i]).ljust(lebar[i]) for i in range(len(kepala))]
        print("| " + " | ".join(teks) + " |")
        if baris is kepala: print(garis)
    print(garis)

def kategori(rasio):
    if rasio is None: return "Tidak tersedia"
    return "Ideal" if rasio >= 2 else "Cukup" if rasio >= 1 else "Kurang"

def perubahan(baru, lama, rasio=False):
    beda = baru - lama
    return "tetap" if beda == 0 else ("naik " if beda > 0 else "turun ") + format_angka(abs(beda), 2 if rasio else 0)

def menu_akun(akun, daftar=False):
    print("\nREGISTRASI" if daftar else "\nLOGIN")
    nama = input("Username: ").strip()
    sandi = input("Password: ").strip()
    if daftar:
        if not nama or not sandi:
            print("Username dan password tidak boleh kosong.")
        elif any(a["username"].lower() == nama.lower() for a in akun):
            print("Username sudah terdaftar.")
        else:
            with open(FILE_AKUN, "a", encoding="utf-8", newline="") as file:
                tulis = csv.writer(file)
                if file.tell() == 0: tulis.writerow(["username", "password"])
                tulis.writerow([nama, sandi])
            akun.append({"username": nama, "password": sandi})
            print("Registrasi berhasil. Silakan login (menu 2).")
        return None
    cocok = any(a["username"].lower() == nama.lower() and a["password"] == sandi for a in akun)
    if cocok:
        print(f"Login berhasil. Selamat datang, {nama}!")
        return nama
    print("Username atau password tidak sesuai.")

def jawaban(prompt):
    while True:
        hasil = input(prompt).strip().lower()
        if hasil in ("ya", "tidak", "batal"): return hasil
        print("\nInput tidak valid. Masukkan ya atau tidak.")

def menu_konsultasi(nama, data):
    print()
    print(f"Halo, {nama}. Konsultasi ketersediaan tempat tidur rumah sakit.")
    print("Ketik 'batal' untuk kembali ke menu.")
    print()
    if jawaban("Apakah Anda atau keluarga sedang membutuhkan perawatan rumah sakit? (ya/tidak): ") != "ya":
        print("\nKonsultasi selesai.")
        return
    while True:
        darurat = jawaban("\nApakah pasien dalam kondisi darurat dan perlu rawat inap segera? (ya/tidak): ")
        if darurat == "batal": return
        if darurat == "ya": print("\nUntuk kondisi darurat, segera cari IGD terdekat atau hubungi layanan darurat setempat.")
        while True:
            kata = input("\nProvinsi mana yang ingin dicek: ").strip()
            if kata.lower() == "batal": return
            hasil = [d for d in data if kata.lower() == d["prov"].lower()]
            if not hasil:
                hasil = [d for d in data if kata.lower() in d["prov"].lower()]
            if len(hasil) == 1:
                break
            if hasil:
                print("Ditemukan beberapa provinsi: " + ", ".join(d["prov"] for d in hasil))
            else:
                print("\nProvinsi tidak ditemukan. Masukkan nama lain.")
        prov = hasil[0]
        rasio, lama = prov["TT Rasio 2024"], prov["TT Rasio 2023"]
        peringkat = sum(d["TT Rasio 2024"] > rasio for d in data) + 1
        print()
        print(f"INFORMASI TEMPAT TIDUR RS: {prov['prov'].upper()}")
        print(f"Jumlah RS 2024            : {format_angka(prov['RS 2024'])} ({perubahan(prov['RS 2024'], prov['RS 2023'])} dari 2023)")
        print(f"Jumlah tempat tidur 2024  : {format_angka(prov['TT Jumlah 2024'])} ({perubahan(prov['TT Jumlah 2024'], prov['TT Jumlah 2023'])} dari 2023)")
        print(f"Rasio per 1.000 penduduk  : {format_angka(rasio, 1)} ({kategori(rasio)})")
        print(f"Peringkat rasio nasional  : {peringkat} dari {len(data)} provinsi")
        if darurat == "ya":
            simpulan = "Kondisi darurat perlu segera ditangani di IGD. Rasio tahunan tidak menunjukkan kamar kosong."
        elif rasio < 1:
            simpulan = f"Tidak sesuai. Rasio {format_angka(rasio, 1)} berada di bawah batas 1,0."
        elif lama is not None and rasio < lama:
            simpulan = f"Sesuai, tetapi rasio menurun dari {format_angka(lama, 1)} menjadi {format_angka(rasio, 1)}."
        elif rasio == 1:
            simpulan = "Sesuai. Rasio mencapai batas minimal 1,0."
        else:
            simpulan = f"Sesuai. Rasio {format_angka(rasio, 1)} memenuhi batas minimal 1,0."
        print(f"Kesimpulan                : {simpulan}")
        print()
        if jawaban("Apakah ingin memeriksa provinsi lain? (ya/tidak): ") != "ya":
            print("\nKonsultasi selesai.")
            return

def menu_data(data, pilihan):
    for baris in ("\nPILIH TAHUN", "1. 2023", "2. 2024", "0. Kembali"):
        print(baris)
    pilih = input("Pilih tahun: ").strip()
    if pilih == "0": return
    if pilih not in ("1", "2"):
        print("Pilihan tahun tidak valid.")
        return
    tahun = "2023" if pilih == "1" else "2024"
    if pilihan == "4":
        rs, tt = f"RS {tahun}", f"TT Jumlah {tahun}"
        total_rs, total_tt = sum(d[rs] for d in data), sum(d[tt] for d in data)
        isi = [[nomor, d["prov"], format_angka(d[rs]),
                format_angka(d[rs] / total_rs * 100, 2) + "%" if total_rs else "0,00%",
                format_angka(d[tt]), format_angka(d[tt] / total_tt * 100, 2) + "%" if total_tt else "0,00%"]
               for nomor, d in zip(range(1, len(data) + 1), sorted(data, key=lambda x: x[rs], reverse=True))]
        isi.append(["", "TOTAL", format_angka(total_rs), "100,00%" if total_rs else "0,00%",
                    format_angka(total_tt), "100,00%" if total_tt else "0,00%"])
        print(f"\nJUMLAH RS DAN TEMPAT TIDUR TIAP PROVINSI ({tahun})")
        tabel(["No", "Provinsi", "Jml RS", "% RS", "Jumlah TT", "% TT"], isi, (0, 2, 3, 4, 5))
        for nama, kolom, fungsi in (("RS terbanyak", rs, max), ("RS tersedikit", rs, min),
                                    ("TT terbanyak", tt, max), ("TT tersedikit", tt, min)):
            prov = fungsi(data, key=lambda d: d[kolom])
            print(f"{nama:<14}: {prov['prov']} ({format_angka(prov[kolom])})")
        return
    kolom = f"TT Rasio {tahun}"
    while True:
        for baris in ("\nKLASIFIKASI RASIO", "1. Ideal", "2. Cukup", "3. Kurang", "4. Semua", "0. Kembali"):
            print(baris)
        pilih = input("Pilih: ").strip()
        if pilih == "0": return
        if pilih not in ("1", "2", "3", "4"):
            print("Pilihan tidak valid.")
            continue
        nama_kategori = {"1": "Ideal", "2": "Cukup", "3": "Kurang"}.get(pilih)
        hasil = [d for d in data if pilih == "4" or
                 (d[kolom] is not None and kategori(d[kolom]) == nama_kategori)]
        hasil.sort(key=lambda d: d[kolom] if d[kolom] is not None else -1, reverse=True)
        print(f"\nKLASIFIKASI RASIO {tahun}: {(nama_kategori or 'SEMUA').upper()}")
        print(f"Jumlah provinsi: {len(hasil)} dari {len(data)} ({format_angka(len(hasil) / len(data) * 100, 2)}%)")
        isi = []
        for d in hasil:
            isi.append([len(isi) + 1, d["prov"], "Tidak tersedia" if d[kolom] is None else format_angka(d[kolom], 2), kategori(d[kolom])])
        tabel(["No", "Provinsi", "Rasio", "Kategori"], isi, (0, 2))

def menu_ringkasan(data):
    ringkasan = {}
    for tahun in ("2023", "2024"):
        rs, tt, kolom = f"RS {tahun}", f"TT Jumlah {tahun}", f"TT Rasio {tahun}"
        rasio = [d[kolom] for d in data if d[kolom] is not None]
        atas, bawah = (max(rasio), min(rasio)) if rasio else (None, None)
        tertinggi = ", ".join(d["prov"] for d in data if d[kolom] == atas) if rasio else "Tidak tersedia"
        terendah = ", ".join(d["prov"] for d in data if d[kolom] == bawah) if rasio else "Tidak tersedia"
        ringkasan[tahun] = [len(data), len(rasio), format_angka(sum(d[rs] for d in data)),
                            format_angka(sum(d[tt] for d in data)),
                            format_angka(statistics.mean(rasio), 2) if rasio else "Tidak tersedia",
                            f"{tertinggi} ({format_angka(atas, 2)})" if rasio else tertinggi,
                            f"{terendah} ({format_angka(bawah, 2)})" if rasio else terendah]
    print("\nRINGKASAN STATISTIK TEMPAT TIDUR RS")
    label = ["Jumlah provinsi", "Provinsi punya rasio", "Total rumah sakit", "Total tempat tidur",
             "Rata-rata rasio", "Rasio tertinggi", "Rasio terendah"]
    tabel(["Indikator", "2023", "2024"], [[label[i], ringkasan["2023"][i], ringkasan["2024"][i]]
          for i in range(len(label))])
    print("\nPERUBAHAN DATA 2023-2024")
    isi = [[nomor, d["prov"], perubahan(d["RS 2024"], d["RS 2023"]),
            perubahan(d["TT Jumlah 2024"], d["TT Jumlah 2023"]),
            "-" if d["TT Rasio 2023"] is None else perubahan(d["TT Rasio 2024"], d["TT Rasio 2023"], True)]
           for nomor, d in zip(range(1, len(data) + 1), data)]
    tabel(["No", "Provinsi", "Perubahan RS", "Perubahan TT", "Perubahan rasio"], isi, (0,))
    print("PERUBAHAN TOTAL NASIONAL")
    print(f"Jumlah rumah sakit  : {perubahan(sum(d['RS 2024'] for d in data), sum(d['RS 2023'] for d in data))}")
    print(f"Jumlah tempat tidur : {perubahan(sum(d['TT Jumlah 2024'] for d in data), sum(d['TT Jumlah 2023'] for d in data))}")


data, ditolak, akun = None, [], []
wajib = ["Provinsi"] + KOLOM + ["TT Rasio 2023", "TT Rasio 2024"]
try:
    with open(FILE_DATA, encoding="utf-8-sig", newline="") as file:
        pembaca = csv.DictReader(file)
        if not pembaca.fieldnames:
            print("File tidak memiliki header.")
        else:
            kolom_hilang = [kolom for kolom in wajib if kolom not in pembaca.fieldnames]
            if kolom_hilang:
                print("Kolom tidak ditemukan: " + ", ".join(kolom_hilang))
            else:
                data = []
                for baris in pembaca:
                    valid, hasil = validasi_input(baris)
                    if valid:
                        data.append(hasil)
                    else:
                        ditolak.append((pembaca.line_num, hasil))
                print(f"Data dibaca: {len(data)} valid, {len(ditolak)} ditolak.")
                if ditolak:
                    print("PEMERIKSAAN DATASET")
                    for nomor, alasan in ditolak:
                        print(f"Baris {nomor}: {alasan}")
                    print("Data yang ditolak tidak digunakan dalam analisis.")
                elif data:
                    print("Tidak ada data yang ditolak saat validasi.")
                else:
                    print("Dataset tidak memiliki baris data.")
except FileNotFoundError:
    print("File CSV tidak ditemukan.")
except OSError:
    print("File CSV tidak dapat dibaca.")
try:
    with open(FILE_AKUN, encoding="utf-8", newline="") as file:
        akun = list(csv.DictReader(file))
except FileNotFoundError: pass
pengguna = None
while data is not None:
    print()
    print("MENU UTAMA")
    print("1. Registrasi")
    print("2. Login")
    print("3. Konsultasi Tempat Tidur")
    print("4. Jumlah RS & Tempat Tidur")
    print("5. Klasifikasi Rasio")
    print("6. Ringkasan & Perubahan 2023-2024")
    print("7. Keluar")
    pilih = input("Pilih menu: ").strip()
    if pilih == "1": menu_akun(akun, True)
    elif pilih == "2": pengguna = menu_akun(akun)
    elif pilih in ("3", "4", "5", "6"):
        if not pengguna: print("Silakan login dahulu (menu 2).")
        elif not data: print("Tidak terdapat data valid untuk dianalisis.")
        elif pilih == "3": menu_konsultasi(pengguna, data)
        elif pilih in ("4", "5"): menu_data(data, pilih)
        else: menu_ringkasan(data)
    elif pilih == "7":
        print("Terima kasih. Program selesai.")
        break
    else: print("Pilihan tidak valid. Masukkan angka 1 sampai 7.")
if data is None:
    print("Program selesai.")
