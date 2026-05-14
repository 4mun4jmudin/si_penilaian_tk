import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import get_db_connection

def update_schema_ortu():
    conn = get_db_connection()
    if not conn:
        print("Gagal koneksi ke database.")
        return

    try:
        cursor = conn.cursor()
        
        # Tambahkan kolom baru satu per satu dengan penanganan duplikat
        columns_to_add = [
            ("id_user_ortu", "INT NULL"),
            ("alamat", "TEXT NULL"),
            ("jenis_kelamin", "VARCHAR(20) NULL"),
            ("foto_anak", "VARCHAR(255) NULL"),
            ("foto_ortu", "VARCHAR(255) NULL")
        ]
        
        for col_name, col_def in columns_to_add:
            cursor.execute(f"SHOW COLUMNS FROM siswa LIKE '{col_name}'")
            result = cursor.fetchone()
            if not result:
                cursor.execute(f"ALTER TABLE siswa ADD COLUMN {col_name} {col_def}")
                print(f"Berhasil menambahkan kolom '{col_name}'.")
            else:
                print(f"Kolom '{col_name}' sudah ada.")
                
        # Buat dummy link untuk akun ortu_demo agar bisa digunakan testing
        cursor.execute("SELECT id FROM users WHERE username = 'ortu_demo'")
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            cursor.execute("SELECT id_siswa FROM siswa LIMIT 1")
            siswa = cursor.fetchone()
            if siswa:
                siswa_id = siswa[0]
                cursor.execute("UPDATE siswa SET id_user_ortu = %s WHERE id_siswa = %s", (user_id, siswa_id))
                print(f"Berhasil me-link ortu_demo (ID:{user_id}) ke Siswa (ID:{siswa_id})")

        conn.commit()
        print("Update schema selesai.")
            
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_schema_ortu()
