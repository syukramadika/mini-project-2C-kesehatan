import csv
import statistics

nama_file = "data/rumah_sakit_per_provinsi_2023_2024.csv"
kolom_angka = ["RS 2023", "TT Jumlah 2023", "TT Rasio 2023",
               "RS 2024", "TT Jumlah 2024", "TT Rasio 2024"]
kolom_wajib = ["Provinsi"] + kolom_angka

def validasi_input(baris):
    provinsi = (baris.get("Provinsi") or "").strip()
    if not provinsi:
        return False, "Nama provinsi kosong."

    data_bersih = {"prov": provinsi}
    for kolom in kolom_angka:
        teks = (baris.get(kolom) or "").strip()
        if kolom == "TT Rasio 2023" and teks == "":
            data_bersih[kolom] = None
            continue
        if teks == "":
            return False, f"Data {kolom} kosong."

        try:
            nilai = float(teks)
        except (ValueError, TypeError):
            return False, f"Data {kolom} bukan angka."

        if nilai != nilai or nilai in (float("inf"), float("-inf")):
            return False, f"Data {kolom} tidak valid."
        if nilai < 0:
            return False, f"Data {kolom} berupa angka negatif."
        data_bersih[kolom] = nilai

    return True, data_bersih


def format_angka(nilai):
    return f"{nilai:,.0f}".replace(",", ".")


def ringkasan_statistik(data_valid, tahun):
    kolom_rs = f"RS {tahun}"
    kolom_tt = f"TT Jumlah {tahun}"
    kolom_rasio = f"TT Rasio {tahun}"
    data_rasio = [isi[kolom_rasio] for isi in data_valid]

    total_rs = sum(isi[kolom_rs] for isi in data_valid)
    total_tt = sum(isi[kolom_tt] for isi in data_valid)
    print(f"\nRINGKASAN STATISTIK {tahun}")
    print(f"Jumlah provinsi      : {len(data_valid)}")
    print(f"Total rumah sakit    : {format_angka(total_rs)}")
    print(f"Total tempat tidur   : {format_angka(total_tt)}")
    print(f"Rata-rata rasio      : {statistics.mean(data_rasio):.2f}")
    tertinggi = max(data_rasio)
    terendah = min(data_rasio)
    provinsi_tertinggi = [isi["prov"] for isi in data_valid
                          if isi[kolom_rasio] == tertinggi]
    provinsi_terendah = [isi["prov"] for isi in data_valid
                         if isi[kolom_rasio] == terendah]

    print(f"Rasio tertinggi      : {', '.join(provinsi_tertinggi)} ({tertinggi:.2f})")
    print(f"Rasio terendah       : {', '.join(provinsi_terendah)} ({terendah:.2f})")


print("=========================================================")
print("Analisis Ketersediaan Tempat Tidur Rumah Sakit")
print("       pada Setiap Provinsi di Indonesia")
print("=========================================================\n")

data_valid = []
daftar_invalid = []
data_berhasil = False

try:
    with open(nama_file, "r", encoding="utf-8-sig", newline="") as file:
        pembaca = csv.DictReader(file)
        if not pembaca.fieldnames:
            print("File CSV tidak memiliki header.")
        else:
            kolom_hilang = [kolom for kolom in kolom_wajib
                            if kolom not in pembaca.fieldnames]
            if kolom_hilang:
                print("Kolom tidak ditemukan: " + ", ".join(kolom_hilang))
            else:
                data_berhasil = True
                for baris in pembaca:
                    valid, hasil = validasi_input(baris)
                    if valid:
                        data_valid.append(hasil)
                    else:
                        daftar_invalid.append((pembaca.line_num, hasil))

                print(f"Data dibaca: {len(data_valid)} valid, {len(daftar_invalid)} ditolak.")
                if daftar_invalid:
                    print("\nPEMERIKSAAN DATASET")
                    for nomor, alasan in daftar_invalid:
                        print(f"Baris {nomor}: {alasan}")
                elif data_valid:
                    print("Tidak ada data yang ditolak saat validasi.")
                else:
                    print("Dataset tidak memiliki baris data.")
except FileNotFoundError:
    print("File CSV tidak ditemukan.")
except OSError:
    print("File CSV tidak dapat dibaca.")

if data_berhasil:
    while True:
        print("\nMENU UTAMA")
        print("1. Ringkasan Statistik")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            print("\nPILIH TAHUN")
            print("1. 2023")
            print("2. 2024")
            print("0. Kembali")
            tahun = input("Pilih tahun: ").strip()
            if tahun == "1":
                ringkasan_statistik(data_valid, "2023")
            elif tahun == "2":
                ringkasan_statistik(data_valid, "2024")
            elif tahun != "0":
                print("Pilihan tahun tidak valid.")
        elif pilihan == "0":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("Pilihan tidak valid. Masukkan angka 0 atau 1.")
else:
    print("Program selesai.")
