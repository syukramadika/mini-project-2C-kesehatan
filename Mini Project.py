import csv
import math
import statistics

nama_file = "data/rumah_sakit_per_provinsi_2023_2024.csv"


def validasi_input(baris):
    nama_provinsi = (baris.get("Provinsi") or "").strip()
    if nama_provinsi == "":
        return False, "Nama provinsi kosong."

    try:
        jumlah_rs_2023 = float(baris["RS 2023"])
        jumlah_tt_2023 = float(baris["TT Jumlah 2023"])
        jumlah_rs_2024 = float(baris["RS 2024"])
        jumlah_tt_2024 = float(baris["TT Jumlah 2024"])
        rasio_2024 = float(baris["TT Rasio 2024"])
    except (ValueError, TypeError, KeyError):
        return False, "Data numerik tidak valid atau kolom tidak ditemukan."

    # Rasio 2023 boleh kosong (dicatat sebagai None)
    rasio_2023 = (baris.get("TT Rasio 2023") or "").strip()
    if rasio_2023 == "":
        rasio_2023 = None
    else:
        try:
            rasio_2023 = float(rasio_2023)
        except (ValueError, TypeError):
            return False, "Data rasio 2023 tidak valid."

    if not math.isfinite(jumlah_rs_2023) or jumlah_rs_2023 < 0:
        return False, "Jumlah RS 2023 tidak valid atau negatif."
    if not math.isfinite(jumlah_tt_2023) or jumlah_tt_2023 < 0:
        return False, "Jumlah TT 2023 tidak valid atau negatif."
    if not math.isfinite(jumlah_rs_2024) or jumlah_rs_2024 < 0:
        return False, "Jumlah RS 2024 tidak valid atau negatif."
    if not math.isfinite(jumlah_tt_2024) or jumlah_tt_2024 < 0:
        return False, "Jumlah TT 2024 tidak valid atau negatif."
    if not math.isfinite(rasio_2024) or rasio_2024 < 0:
        return False, "Rasio 2024 tidak valid atau negatif."
    if rasio_2023 is not None:
        if not math.isfinite(rasio_2023) or rasio_2023 < 0:
            return False, "Rasio 2023 tidak valid atau negatif."

    data_bersih = {
        "prov": nama_provinsi,
        "RS 2023": jumlah_rs_2023,
        "TT Jumlah 2023": jumlah_tt_2023,
        "TT Rasio 2023": rasio_2023,
        "RS 2024": jumlah_rs_2024,
        "TT Jumlah 2024": jumlah_tt_2024,
        "TT Rasio 2024": rasio_2024,
    }
    return True, data_bersih


def baca_data(nama_file):
    data_valid = []
    daftar_invalid = []

    try:
        with open(nama_file, "r", encoding="utf-8-sig", newline="") as file:
            pembaca = csv.DictReader(file)
            for baris in pembaca:
                valid, hasil = validasi_input(baris)
                if valid:
                    data_valid.append(hasil)
                else:
                    daftar_invalid.append((pembaca.line_num, hasil))

        print(f"Data dibaca: {len(data_valid)} valid, {len(daftar_invalid)} ditolak.")
        return data_valid, daftar_invalid

    except FileNotFoundError:
        print("File CSV tidak ditemukan.")
        return None, None


def format_angka(nilai):
    return f"{nilai:,.0f}".replace(",", ".")


def ringkasan_statistik(data_valid, tahun):
    kolom_rs = f"RS {tahun}"
    kolom_tt = f"TT Jumlah {tahun}"
    kolom_rasio = f"TT Rasio {tahun}"

    data_rasio = [isi for isi in data_valid if isi[kolom_rasio] is not None]
    if not data_rasio:
        print("Tidak ada data rasio valid untuk tahun ini.")
        return

    total_rs = sum(isi[kolom_rs] for isi in data_valid)
    total_tt = sum(isi[kolom_tt] for isi in data_valid)
    daftar_rasio = [isi[kolom_rasio] for isi in data_rasio]

    tertinggi = data_rasio[0]
    terendah = data_rasio[0]
    for isi in data_rasio:
        if isi[kolom_rasio] > tertinggi[kolom_rasio]:
            tertinggi = isi
        if isi[kolom_rasio] < terendah[kolom_rasio]:
            terendah = isi

    print(f"\n=== RINGKASAN STATISTIK {tahun} ===")
    print(f"Jumlah provinsi      : {len(data_valid)}")
    print(f"Total rumah sakit    : {format_angka(total_rs)}")
    print(f"Total tempat tidur   : {format_angka(total_tt)}")
    print(f"Rata-rata rasio      : {statistics.mean(daftar_rasio):.2f}")
    print(f"Rasio tertinggi      : {tertinggi['prov']} ({tertinggi[kolom_rasio]:.2f})")
    print(f"Rasio terendah       : {terendah['prov']} ({terendah[kolom_rasio]:.2f})")


data_valid, daftar_invalid = baca_data(nama_file)

if data_valid is not None:
    print("\n=== PEMERIKSAAN DATA ===")
    if daftar_invalid:
        for nomor, alasan in daftar_invalid:
            print(f"- Baris {nomor}: {alasan}")
    else:
        print("Tidak ada data yang ditolak saat validasi.")

    ringkasan_statistik(data_valid, "2023")
    ringkasan_statistik(data_valid, "2024")