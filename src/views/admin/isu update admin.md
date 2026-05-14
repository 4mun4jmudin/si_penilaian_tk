# PRIORITAS UPDATE APLIKASI ADMIN TK PENILAIAN

## 1. UPDATE DASHBOARD ADMIN

### Tambahkan Statistik Utama

Dashboard sekarang masih terlalu basic.

Tambahkan:

* Total Guru
* Total Siswa
* Total Penilaian
* Total Laporan
* Pengumuman Aktif
* Penilaian Hari Ini
* Siswa Perlu Evaluasi

---

### Tambahkan Quick Action

Buat tombol cepat:

* Tambah Guru
* Tambah Siswa
* Input Penilaian
* Buat Laporan

Supaya admin tidak harus buka menu dulu.

---

### Tambahkan Aktivitas Terbaru

Contoh:

* Guru baru ditambahkan
* Penilaian terbaru
* Pengumuman terbaru
* Laporan terakhir dibuat

Dashboard jadi terasa hidup.

---

### Tambahkan Grafik Statistik

Misalnya:

* perkembangan jumlah penilaian
* siswa per kelas
* status perkembangan siswa

---

### Tambahkan Empty State

Kalau data kosong:

* icon
* text informatif
* tombol tambah data

---

---

# 2. UPDATE KELOLA GURU

## WAJIB

### Tambahkan Dialog Konfirmasi Hapus

Sebelum hapus:

* tampilkan popup konfirmasi

---

### Hash Password

Jangan simpan password plain text.

Gunakan:

* bcrypt
* werkzeug security
* hashlib minimal

---

### Validasi Input

Tambahkan:

* NIP hanya angka
* minimal karakter
* nama tidak boleh kosong
* username unik

---

### Tambahkan Snackbar Modern

Ganti toast dengan:

* Snackbar
* success
* error
* warning

Lebih premium.

---

## REKOMENDASI

### Tambahkan Foto Guru

Supaya lebih profesional.

---

### Tambahkan Detail Guru

Misalnya:

* alamat
* no HP
* email
* jabatan

---

### Tambahkan Status Akun

* aktif
* nonaktif

---

### Tambahkan Reset Password

Admin bisa reset password guru.

---

### Tambahkan Pagination / Lazy Loading

Kalau data guru banyak aplikasi tetap ringan.

---

---

# 3. UPDATE KELOLA SISWA

## WAJIB

### Ganti Input Tanggal Manual

Gunakan:

* MDDatePicker

Karena input manual rawan salah.

---

### Gunakan Dropdown Kelas

Pilihan:

* TK-A
* TK-B

Supaya data konsisten.

---

### Tambahkan Validasi

* nama wajib
* kelas wajib
* tanggal valid

---

### Tambahkan Konfirmasi Hapus

---

## REKOMENDASI

### Tambahkan Foto Siswa

---

### Tambahkan Detail Tambahan

* jenis kelamin
* alamat
* agama
* nomor induk

---

### Tambahkan Filter

Filter berdasarkan:

* kelas
* umur
* perkembangan

---

### Tambahkan Search Lebih Advanced

Cari:

* nama
* orang tua
* kelas

---

---

# 4. UPDATE KELOLA PENGUMUMAN

## WAJIB

### Tambahkan Edit Pengumuman

Sekarang baru:

* tambah
* hapus

Belum ada edit.

---

### Tambahkan Konfirmasi Hapus

---

### Batasi Preview Text

Jangan tampilkan isi penuh di list.

Gunakan:

* max 1–2 baris

---

### Tambahkan Search Pengumuman

---

## REKOMENDASI

### Tambahkan Kategori

Misalnya:

* informasi
* libur
* kegiatan
* penting

---

### Tambahkan Status Publish

* draft
* publish

---

### Tambahkan Target Pengumuman

* semua orang tua
* kelas tertentu

---

### Tambahkan Lampiran Gambar/File

---

---

# 5. UPDATE SISTEM PENILAIAN

## PRIORITAS TERTINGGI

Karena inti aplikasi ada di sini.

---

### Buat Halaman Input Penilaian

Fitur:

* pilih siswa
* pilih indikator
* pilih nilai BB/MB/BSH/BSB
* catatan guru

---

### Tambahkan Auto Generate Deskripsi

Contoh:

“Ananda berkembang sesuai harapan dalam motorik halus.”

---

### Tambahkan Riwayat Penilaian

---

### Tambahkan Filter Penilaian

* per siswa
* per kelas
* per tanggal

---

### Tambahkan Rekap Nilai

---

---

# 6. UPDATE LAPORAN

## WAJIB

### Generate PDF Profesional

Isi:

* identitas siswa
* nilai perkembangan
* deskripsi otomatis
* tanda tangan guru

---

### Tambahkan Preview Laporan

---

### Tambahkan Export

* PDF
* Excel

---

### Tambahkan Cetak Langsung

---

---

# 7. UPDATE UI/UX PREMIUM

## DESIGN SYSTEM

### Konsistenkan Warna

Gunakan hanya:

* Navy
* Emerald
* Amber
* White

---

### Konsistenkan Radius

Semua card:

* radius sama

---

### Konsistenkan Shadow

---

### Tambahkan Animasi Halus

* hover
* press
* transition

---

### Tambahkan Skeleton Loading

---

### Tambahkan Responsive Layout

---

### Tambahkan Dark Mode

---

---

# 8. UPDATE KEAMANAN

## SANGAT PENTING

### Hash Password

---

### Validasi SQL Input

---

### Session Timeout

---

### Role Access

Pastikan:

* admin tidak bisa diakses guru
* guru tidak bisa akses admin panel

---

### Logging Aktivitas

Simpan:

* login
* tambah data
* hapus data
* edit data

---

---

# 9. UPDATE DATABASE

## REKOMENDASI

### Tambahkan Timestamp

Semua tabel:

* created_at
* updated_at

---

### Tambahkan Foreign Key Lengkap

---

### Tambahkan Soft Delete

---

### Rapikan Relasi User

---

---

# 10. UPDATE PROFESSIONAL FEATURES

## AGAR TERLIHAT LEVEL PRODUK

### Notifikasi Real-Time

---

### Backup Database

---

### Restore Database

---

### Pengaturan Sekolah

* logo
* nama sekolah
* kepala sekolah
* semester

---

### Multi Tahun Ajaran

---

### Multi Kelas

---

### Dashboard Analitik

---

# PRIORITAS PALING PENTING SEKARANG

## Fokus dulu ke ini:

### 1. Penilaian

### 2. Laporan PDF

### 3. Dashboard statistik

### 4. Keamanan password

### 5. UX premium
