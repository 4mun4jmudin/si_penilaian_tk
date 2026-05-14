# Sistem Penilaian TK Miftahul Jannah v2.0 🏫✨

Sistem Penilaian Digital untuk TK Miftahul Jannah yang dibangun menggunakan **Python**, **Kivy**, **KivyMD**, dan **MySQL**. Aplikasi ini dirancang untuk memudahkan Guru dalam menginput nilai harian dan catatan anekdot, serta memudahkan Orang Tua dalam memantau perkembangan anak secara real-time.

---

## 🚀 Fitur Utama
- **Admin**: Kelola data Guru, Siswa, dan Pengumuman.
- **Guru**: Input nilai harian (BB, MB, BSH, BSB), Catatan Anekdot, dan Generate Laporan PDF.
- **Orang Tua**: Dashboard perkembangan anak, Riwayat laporan, dan Notifikasi pengumuman.
- **Modern UI**: Antarmuka premium dengan desain responsif dan animasi halus.

---

## 🛠️ Panduan Instalasi (Lengkap dari Nol)

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer lokal Anda:

### 1. Prasyarat
Pastikan Anda sudah menginstal:
- **Python 3.10 atau lebih baru** ([Unduh di sini](https://www.python.org/downloads/))
- **MySQL Server** (Bisa menggunakan XAMPP atau MySQL Installer)
- **Git** (Opsional, untuk clone repository)

### 2. Clone Repository
Buka terminal atau command prompt, lalu jalankan:
```bash
git clone https://github.com/4mun4jmudin/si_penilaian_tk.git
cd si_penilaian_tk
```

### 3. Buat Virtual Environment (Disarankan)
Agar library tidak bentrok dengan sistem global:
```bash
# Windows
python -m venv .venv
.venv\\Scripts\\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalasi Library
Instal semua dependensi yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 5. Konfigurasi Database
1. Buka **phpMyAdmin** atau MySQL Client lainnya.
2. Buat database baru dengan nama: `db_penilaian_perkembangan_siswa_tk`
3. Import file SQL (jika ada) atau pastikan tabel sudah sesuai dengan schema.
4. Buat file `.env` di root folder project dan isi dengan kredensial MySQL Anda:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=
   DB_NAME=db_penilaian_perkembangan_siswa_tk
   ```

### 6. Jalankan Aplikasi
Masuk ke folder `src` dan jalankan file `main.py`:
```bash
cd src
python main.py
```

---

## 🔑 Akun Demo (Default)
| Peran | Username | Password |
|-------|----------|----------|
| **Admin** | `admin1` | `admin123` |
| **Guru** | `guru1` | `123456` |
| **Orang Tua** | `ortu1` | `123456` |

---

## 📁 Struktur Folder
```text
si_penilaian_tk/
├── assets/             # Gambar, Icon, dan Font
├── src/                # Source Code Utama
│   ├── config/         # Konfigurasi DB & Session
│   ├── models/         # Business Logic (MVC - Model)
│   ├── views/          # Antarmuka (MVC - View)
│   └── main.py         # Entry Point Aplikasi
├── .env                # Variabel Lingkungan (DB Config)
├── requirements.txt    # Daftar Library
└── README.md           # Dokumentasi
```

---

## 🤝 Kontribusi
Jika ingin berkontribusi, silakan lakukan **Fork** repository ini dan kirimkan **Pull Request**. Kami sangat terbuka untuk perbaikan UI/UX dan penambahan fitur baru.

---

**TK Islam Plus Miftahul Jannah**  
*Mencetak Generasi Cerdas, Kreatif, dan Berakhlak Mulia.*
