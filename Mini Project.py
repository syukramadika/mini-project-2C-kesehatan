import csv

nama_file = "data/rumah_sakit_per_provinsi_2023_2024.csv"


def baca_data(nama_file):
    data = []

    try:
        with open(nama_file, "r", encoding="utf-8-sig") as file:
            pembaca = csv.DictReader(file)
            for baris in pembaca:
                data.append(baris)

        print("Data berhasil dibaca.")
        print(f"Jumlah data provinsi: {len(data)}")
        return data

    except FileNotFoundError:
        print("File CSV tidak ditemukan.")
        return None


def validasi_data(data):
    kolom_penting = [
        "Provinsi", "RS 2023", "TT Jumlah 2023",
        "RS 2024", "TT Jumlah 2024"
    ]

    data_valid = True

    try:
        for nomor, baris in enumerate(data, start=1):
            for kolom in kolom_penting:
                if baris[kolom] == "" or baris[kolom] is None:
                    print(f"Data baris {nomor} tidak valid: kolom {kolom} kosong.")
                    data_valid = False

        if data_valid:
            print("Validasi data selesai: tidak ditemukan data kosong pada kolom penting.")
        else:
            print("Validasi data selesai: terdapat data yang perlu diperiksa.")

    except KeyError:
        print("Kolom CSV tidak sesuai dengan format yang dibutuhkan.")


data = baca_data(nama_file)

if data is not None:
    validasi_data(data)