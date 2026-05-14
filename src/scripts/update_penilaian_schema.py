import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import get_db_connection

def update_schema():
    conn = get_db_connection()
    if not conn:
        print("Gagal koneksi ke database.")
        return

    try:
        cursor = conn.cursor()
        # Periksa apakah kolom sudah ada
        cursor.execute("SHOW COLUMNS FROM penilaian LIKE 'catatan'")
        result = cursor.fetchone()
        
        if result:
            print("Kolom 'catatan' sudah ada di tabel 'penilaian'.")
        else:
            # Tambahkan kolom
            cursor.execute("ALTER TABLE penilaian ADD COLUMN catatan TEXT NULL")
            conn.commit()
            print("Berhasil menambahkan kolom 'catatan' ke tabel 'penilaian'.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_schema()
