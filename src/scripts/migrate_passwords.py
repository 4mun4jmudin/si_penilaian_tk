import sys
import os

# Menambahkan parent directory ke system path agar bisa import dari src.config dan src.models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bcrypt
from config.database import get_db_connection

def migrate():
    print("Membuka koneksi ke database...")
    conn = get_db_connection()
    if not conn:
        print("Gagal terhubung ke database. Pastikan XAMPP berjalan.")
        return

    try:
        cursor = conn.cursor(dictionary=True)
        # Ambil semua user
        cursor.execute("SELECT id, username, password FROM users")
        users = cursor.fetchall()

        if not users:
            print("Tidak ada data user di tabel users.")
            return

        migrated_count = 0
        skipped_count = 0

        for user in users:
            user_id = user['id']
            username = user['username']
            password = user['password']

            # Deteksi apakah password sudah berbentuk hash bcrypt
            # Hash bcrypt panjangnya persis 60 karakter dan diawali '$2b$', '$2a$', atau '$2y$'
            if len(password) == 60 and (password.startswith('$2b$') or password.startswith('$2a$') or password.startswith('$2y$')):
                print(f"User '{username}' (ID: {user_id}) sudah di-hash. Melewati...")
                skipped_count += 1
                continue

            # Jika belum di-hash (plaintext)
            print(f"Menghash password untuk user '{username}' (ID: {user_id})...")
            
            # Buat hash
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Update ke database
            update_cursor = conn.cursor()
            update_cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
            migrated_count += 1
            
        conn.commit()
        
        print("\n--- Ringkasan Migrasi ---")
        print(f"Total user diproses: {len(users)}")
        print(f"Berhasil di-hash (baru): {migrated_count}")
        print(f"Dilewati (sudah aman): {skipped_count}")
        print("Migrasi selesai!")

    except Exception as e:
        conn.rollback()
        print(f"Terjadi kesalahan saat migrasi: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
