"""
=================================================================
Database Configuration — Sistem Penilaian TK Miftahul Jannah
=================================================================
Modul ini menangani koneksi ke database MySQL menggunakan:
- Environment Variables (.env) untuk keamanan kredensial
- Connection Pooling untuk performa multi-user
- Logging profesional untuk debugging

Author : System Refactored
Version: 2.0 (Production-Ready)
=================================================================
"""

import os
import logging
from pathlib import Path

import mysql.connector
from mysql.connector import Error, pooling
from dotenv import load_dotenv

# ----- Setup Logging -----
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console handler agar tetap terlihat saat development
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%H:%M:%S'
    ))
    logger.addHandler(handler)


# ----- Load Environment Variables -----
# Cari file .env di root project (naik 1 level dari src/config/)
_env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=_env_path)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'db_penilaian_perkembangan_siswa_tk')
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '5'))
DB_POOL_NAME = os.getenv('DB_POOL_NAME', 'tk_miftahul_pool')


# ----- Connection Pool (Singleton) -----
_connection_pool = None


def _init_pool():
    """
    Inisialisasi Connection Pool (hanya dipanggil sekali).
    Connection Pooling memungkinkan banyak guru mengakses DB
    secara bersamaan tanpa error 'Too many connections'.
    """
    global _connection_pool
    try:
        _connection_pool = pooling.MySQLConnectionPool(
            pool_name=DB_POOL_NAME,
            pool_size=DB_POOL_SIZE,
            pool_reset_session=True,
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            collation='utf8mb4_general_ci',
            autocommit=False,
        )
        logger.info(f"✅ Connection Pool '{DB_POOL_NAME}' berhasil dibuat (size={DB_POOL_SIZE})")
    except Error as e:
        logger.error(f"❌ Gagal membuat Connection Pool: {e}")
        _connection_pool = None


def get_db_connection():
    """
    Mengambil koneksi dari pool.
    Jika pool belum diinisialisasi, akan otomatis dibuat.

    Returns:
        mysql.connector.connection.MySQLConnection | None

    Usage:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT ...")
                data = cursor.fetchall()
                conn.commit()  # Jika ada INSERT/UPDATE
            except Exception as e:
                conn.rollback()
                logger.error(f"Query error: {e}")
            finally:
                conn.close()  # Mengembalikan koneksi ke pool
    """
    global _connection_pool

    if _connection_pool is None:
        _init_pool()

    if _connection_pool is None:
        logger.error("Pool tidak tersedia. Pastikan MySQL berjalan dan .env sudah benar.")
        return None

    try:
        connection = _connection_pool.get_connection()
        if connection.is_connected():
            return connection
    except Error as e:
        logger.error(f"Gagal mengambil koneksi dari pool: {e}")

    return None


# ----- Testing Koneksi -----
if __name__ == "__main__":
    print("=" * 50)
    print("  DATABASE CONNECTION TEST")
    print("=" * 50)
    print(f"  Host     : {DB_HOST}")
    print(f"  Port     : {DB_PORT}")
    print(f"  Database : {DB_NAME}")
    print(f"  User     : {DB_USER}")
    print(f"  Pool Size: {DB_POOL_SIZE}")
    print("=" * 50)

    conn = get_db_connection()
    if conn and conn.is_connected():
        print(f"✅ SUKSES: Koneksi ke '{DB_NAME}' berhasil!")
        print(f"ℹ️  MySQL Server: {conn.get_server_info()}")
        conn.close()
        print("   Koneksi dikembalikan ke pool.")
    else:
        print("❌ GAGAL: Tidak bisa terhubung. Cek XAMPP & file .env")