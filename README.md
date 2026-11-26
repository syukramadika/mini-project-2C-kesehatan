# MINI PROJECT PEMROGRAMAN KOMPUTER
## Klasifikasi Tingkat Ketersediaan Tempat Tidur Rumah Sakit pada Setiap Provinsi di Indonesia Berbasis Python

**Kelompok 2C**  
Departemen Teknik Industri  
Fakultas Teknik  
Universitas Andalas  
2026

---

## 1. Deskripsi Program

Mini project ini membahas klasifikasi tingkat ketersediaan tempat tidur rumah sakit pada setiap provinsi di Indonesia menggunakan bahasa pemrograman Python. Program dibuat untuk membaca, memvalidasi, mengolah, dan menampilkan data jumlah rumah sakit, jumlah tempat tidur, estimasi penduduk, serta rasio tempat tidur rumah sakit per 1.000 penduduk pada tahun 2023 dan 2024.

Program ini diharapkan dapat membantu pengguna memperoleh gambaran mengenai perbedaan ketersediaan tempat tidur rumah sakit antarprovinsi melalui proses pengolahan data yang lebih terstruktur.

## 2. Tujuan Program

Program ini dibuat dengan tujuan:
1. Membaca dan memvalidasi dataset rumah sakit dalam format CSV.
2. Mengelompokkan rasio tempat tidur rumah sakit berdasarkan kategori yang ditentukan.
3. Menampilkan jumlah rumah sakit dan tempat tidur pada setiap provinsi.
4. Menyajikan persentase kontribusi setiap provinsi terhadap total nasional.
5. Menampilkan ringkasan statistik data tahun 2023 dan 2024.
6. Membandingkan perubahan jumlah rumah sakit, tempat tidur, dan rasio antara tahun 2023 dan 2024.

## 3. Pengguna Program

Program ditujukan untuk Dinas Kesehatan Provinsi, perencana fasilitas kesehatan, dan peneliti di bidang kesehatan. Program dapat digunakan untuk melihat dan mengevaluasi ketersediaan tempat tidur rumah sakit berdasarkan rasio terhadap jumlah penduduk pada setiap provinsi di Indonesia.

## 4. Dataset dan Sumber Data

Dataset yang digunakan berupa file CSV yang diolah dari tabel *Jumlah Rumah Sakit dan Rasio Tempat Tidur Rumah Sakit per 1.000 Penduduk Menurut Provinsi Tahun 2023–2024* dalam dokumen *Profil Kesehatan Indonesia 2024* yang diterbitkan oleh Kementerian Kesehatan Republik Indonesia.

Sumber data: https://repository.kemkes.go.id/book/1356

Dataset terdiri atas 38 provinsi dengan informasi sebagai berikut:

| No. | Nama Kolom | Keterangan |
|---|---|---|
| 1 | No | Nomor urut provinsi |
| 2 | Provinsi | Nama provinsi |
| 3 | Estimasi Penduduk 2022 | Jumlah estimasi penduduk tahun 2022 |
| 4 | RS 2023 | Jumlah rumah sakit tahun 2023 |
| 5 | TT Jumlah 2023 | Jumlah tempat tidur tahun 2023 |
| 6 | TT Rasio 2023 | Rasio tempat tidur tahun 2023 |
| 7 | Estimasi Penduduk 2023 | Jumlah estimasi penduduk tahun 2023 |
| 8 | RS 2024 | Jumlah rumah sakit tahun 2024 |
| 9 | TT Jumlah 2024 | Jumlah tempat tidur tahun 2024 |
| 10 | TT Rasio 2024 | Rasio tempat tidur tahun 2024 |

## 5. Proses Pengolahan Data

Proses pengolahan data dimulai dengan membaca file CSV menggunakan modul `csv`. Data kemudian diperiksa kelengkapan dan validitasnya sebelum disimpan untuk proses analisis. Baris yang memenuhi ketentuan akan dimasukkan ke dalam list `data`, sedangkan baris yang tidak memenuhi ketentuan disimpan dalam list `ditolak`.

Secara umum, proses pengolahan data meliputi:
1. Membaca file dataset CSV.
2. Memeriksa keberadaan file dan kolom yang dibutuhkan.
3. Memvalidasi setiap baris data.
4. Memisahkan data valid dan tidak valid.
5. Mengolah data berdasarkan tahun yang dipilih.
6. Mengelompokkan rasio ke dalam kategori.
7. Menampilkan hasil analisis melalui menu program.

### Potongan kode pembacaan CSV

```python
with open(FILE_DATA, encoding="utf-8-sig", newline="") as file:
    pembaca = csv.DictReader(file)
```

Kode tersebut digunakan untuk membuka file CSV dan membaca setiap baris berdasarkan nama kolom menggunakan `csv.DictReader()`.

### Potongan kode penyimpanan data

```python
data = []

for baris in pembaca:
    valid, hasil = validasi_input(baris)

    if valid:
        data.append(hasil)
    else:
        ditolak.append((pembaca.line_num, hasil))
```

Kode tersebut memisahkan data berdasarkan hasil validasi. Data yang valid disimpan dalam list `data`, sedangkan data yang ditolak disimpan dalam list `ditolak` beserta nomor baris dan alasan penolakannya.

## 6. Klasifikasi Rasio Tempat Tidur

Klasifikasi rasio digunakan untuk mengelompokkan tingkat ketersediaan tempat tidur rumah sakit berdasarkan nilai rasio per 1.000 penduduk. Program menggunakan tiga kategori, yaitu Ideal, Cukup, dan Kurang.

Ketentuan klasifikasi yang diterapkan dalam kode adalah:

| Kategori | Ketentuan |
|---|---|
| Ideal | Rasio ≥ 2,0 |
| Cukup | 1,0 ≤ Rasio < 2,0 |
| Kurang | Rasio < 1,0 |
| Tidak tersedia | Nilai rasio kosong |

### Potongan kode klasifikasi

```python
def kategori(rasio):
    if rasio is None:
        return "Tidak tersedia"
    return "Ideal" if rasio >= 2 else "Cukup" if rasio >= 1 else "Kurang"
```

Fungsi `kategori()` menerima nilai rasio sebagai parameter, kemudian menentukan kategori berdasarkan kondisi yang telah ditetapkan.

**Contoh hasil klasifikasi:**

| Nilai Rasio | Kategori |
|---:|---|
| 0,40 | Kurang |
| 0,99 | Kurang |
| 1,00 | Cukup |
| 1,38 | Cukup |
| 1,99 | Cukup |
| 2,00 | Ideal |
| 2,60 | Ideal |

Nilai rasio dibaca langsung dari dataset dan tidak dihitung ulang oleh program.

## 7. Perhitungan dan Analisis Data

Program melakukan beberapa proses pengolahan untuk menyajikan informasi yang lebih mudah dipahami.

### a. Perubahan jumlah rumah sakit dan tempat tidur

Perubahan dihitung dengan membandingkan nilai tahun 2024 terhadap tahun 2023.

**Rumus:**

```text
Perubahan = Nilai Tahun 2024 - Nilai Tahun 2023
```

Keterangan:
- Hasil positif menunjukkan kenaikan.
- Hasil negatif menunjukkan penurunan.
- Hasil nol menunjukkan tidak ada perubahan.

**Contoh:**

Jumlah rumah sakit tahun 2023 = 77  
Jumlah rumah sakit tahun 2024 = 81

```text
Perubahan = 81 - 77
          = 4
```

Artinya, jumlah rumah sakit mengalami kenaikan sebanyak 4.

### b. Persentase kontribusi

Persentase kontribusi digunakan untuk menunjukkan bagian jumlah rumah sakit atau tempat tidur suatu provinsi terhadap total keseluruhan.

**Rumus umum:**

```text
Persentase kontribusi =
(Jumlah pada provinsi / Total keseluruhan) x 100%
```

### c. Rata-rata rasio

Rata-rata rasio digunakan untuk memperoleh nilai rata-rata dari data rasio yang tersedia.

```python
statistics.mean(rasio)
```

Fungsi `statistics.mean()` digunakan untuk menghitung rata-rata nilai dalam kumpulan data rasio.

**Catatan:** Rumus perubahan dan persentase kontribusi digunakan untuk menjelaskan proses perhitungan yang relevan dalam program. Nilai rasio tempat tidur sendiri dibaca langsung dari dataset.

## 8. Fitur Program

Program menyediakan beberapa fitur utama yang dapat digunakan melalui menu interaktif:

1. **Registrasi:** membuat akun pengguna baru.
2. **Login:** masuk menggunakan akun yang telah didaftarkan.
3. **Konsultasi Tempat Tidur:** mencari informasi rumah sakit dan tempat tidur berdasarkan provinsi.
4. **Jumlah RS & Tempat Tidur:** menampilkan jumlah rumah sakit dan tempat tidur berdasarkan tahun yang dipilih.
5. **Klasifikasi Rasio:** menampilkan provinsi berdasarkan kategori Ideal, Cukup, Kurang, atau Semua.
6. **Ringkasan & Perubahan 2023–2024:** menampilkan ringkasan statistik dan perbandingan data antartahun.
7. **Keluar:** mengakhiri penggunaan program.

## 9. Teknologi dan Fungsi Python

Program dikembangkan menggunakan bahasa pemrograman Python dengan memanfaatkan beberapa modul bawaan:

| Modul | Kegunaan |
|---|---|
| `csv` | Membaca dan mengolah file CSV |
| `statistics` | Menghitung statistik, termasuk rata-rata |
| `os` | Mendukung pengelolaan file dan direktori |

Selain itu, program menerapkan beberapa konsep dasar pemrograman, yaitu:
- Variabel dan tipe data.
- List dan dictionary.
- Percabangan `if-else`.
- Perulangan `for` dan `while`.
- Fungsi dan parameter.
- File Input/Output.
- Validasi data.

## 10. Validasi Data

Validasi dilakukan melalui fungsi `validasi_input()` untuk memastikan data yang dibaca memenuhi ketentuan sebelum digunakan dalam proses analisis.

Pemeriksaan yang dilakukan meliputi:
1. Nama provinsi tidak boleh kosong.
2. Kolom numerik wajib harus terisi.
3. Data harus dapat dikonversi menjadi angka.
4. Nilai angka tidak boleh negatif.
5. Nilai tidak boleh berupa NaN atau infinity.
6. Kolom jumlah penduduk, rumah sakit, dan tempat tidur harus berupa bilangan bulat.
7. Nilai rasio tahun 2023 boleh kosong dan disimpan sebagai `None`.

Data yang tidak memenuhi ketentuan akan ditolak dan ditampilkan bersama nomor baris serta alasan penolakannya.

## 11. Cara Menjalankan Program

Untuk menjalankan program, pastikan Python telah terpasang pada komputer dan dataset berada pada direktori yang sesuai dengan lokasi file pada kode.

Jalankan program melalui terminal menggunakan perintah:

```bash
python "Mini Project.py"
```

Setelah program berjalan, pengguna dapat mengikuti instruksi yang ditampilkan pada terminal, melakukan registrasi, kemudian login untuk mengakses fitur pengolahan dan analisis data.

## 12. Pengujian Program

Pengujian dilakukan menggunakan lima variasi file CSV untuk mengetahui kemampuan program dalam menghadapi kondisi data yang berbeda.

| No. | Jenis Pengujian | Tujuan |
|---|---|---|
| 1 | Data normal dan lengkap | Memastikan data lengkap dapat diproses |
| 2 | Data batas | Memeriksa ketepatan klasifikasi pada nilai ambang |
| 3 | Dataset kosong | Memastikan program menangani dataset tanpa baris data |
| 4 | Data tidak valid | Memastikan baris yang tidak sesuai dapat ditolak |
| 5 | Regresi/perubahan data | Memeriksa penyajian perubahan data 2023–2024 |

## 13. Batasan Program

Program hanya mengolah data yang tersedia dalam dataset, yaitu nama provinsi, estimasi penduduk, jumlah rumah sakit, jumlah tempat tidur, dan rasio tempat tidur tahun 2023 dan 2024. Nilai rasio dibaca langsung dari file CSV dan tidak dihitung ulang oleh program. Validasi juga belum memeriksa kesesuaian rasio dengan jumlah tempat tidur dan penduduk. Program tidak melakukan prediksi pertumbuhan penduduk maupun memperkirakan kebutuhan pembangunan rumah sakit pada masa mendatang.

## 14. Penutup

Melalui mini project ini, pengolahan data ketersediaan tempat tidur rumah sakit pada setiap provinsi dapat dilakukan secara lebih terstruktur menggunakan Python. Program diharapkan dapat membantu pengguna memperoleh informasi mengenai jumlah rumah sakit, jumlah tempat tidur, rasio ketersediaan, klasifikasi, serta perubahan data antartahun berdasarkan dataset yang digunakan.

---

**Kelompok 2C**  
Mini Project Praktikum Pemrograman Komputer 2026  
Departemen Teknik Industri – Fakultas Teknik  
Universitas Andalas
