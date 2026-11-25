# Mini Project
# Analisis Ketersediaan Tempat Tidur Rumah Sakit
# pada Setiap Provinsi di Indonesia

import csv

nama_file = "rumah_sakit_per_provinsi_2023_2024.csv"
data = []

try:
    with open(nama_file, "r", encoding="utf-8-sig") as file:
        pembaca = csv.DictReader(file)
        for baris in pembaca:
            data.append(baris)

    print("Data berhasil dibaca.")
    print("Jumlah data provinsi:", len(data))

except FileNotFoundError:
    print("File CSV tidak ditemukan.")
