from config.database import get_db_connection

def setup_new_tables():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # 1. Tabel Pengumuman
        query_pengumuman = """
        CREATE TABLE IF NOT EXISTS pengumuman (
            id_pengumuman INT AUTO_INCREMENT PRIMARY KEY,
            judul VARCHAR(255) NOT NULL,
            isi TEXT NOT NULL,
            tanggal DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # 2. Tabel Catatan Anekdot
        query_anekdot = """
        CREATE TABLE IF NOT EXISTS catatan_anekdot (
            id_anekdot INT AUTO_INCREMENT PRIMARY KEY,
            id_siswa INT NOT NULL,
            id_guru INT,
            tanggal DATE NOT NULL,
            catatan TEXT NOT NULL,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa) ON DELETE CASCADE
        );
        """
        
        try:
            cursor.execute(query_pengumuman)
            print("OK: Tabel 'pengumuman' berhasil disiapkan.")
            
            cursor.execute(query_anekdot)
            print("OK: Tabel 'catatan_anekdot' berhasil disiapkan.")
            
            # Tambah data dummy pengumuman untuk testing jika masih kosong
            cursor.execute("SELECT COUNT(*) FROM pengumuman")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO pengumuman (judul, isi) VALUES ('Selamat Datang', 'Selamat datang di Aplikasi Penilaian TK Miftahul Jannah.')")
                conn.commit()
                print("OK: Data dummy pengumuman ditambahkan.")
                
        except Exception as e:
            print(f"Error: Terjadi kesalahan saat membuat tabel: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("❌ Gagal terhubung ke database. Pastikan XAMPP (MySQL) menyala.")

if __name__ == "__main__":
    setup_new_tables()
