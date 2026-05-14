"""
Model: Pengumuman — Kelola Pengumuman Sekolah
==============================================
Menangani operasi CRUD untuk tabel `pengumuman`.
"""

import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)


class PengumumanModel:

    @staticmethod
    def get_all():
        """Mengambil semua pengumuman, urut terbaru."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pengumuman ORDER BY tanggal DESC")
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get all pengumuman error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_latest(limit=5):
        """Mengambil pengumuman terbaru (untuk dashboard orang tua) dalam rentang 1 minggu terakhir."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM pengumuman WHERE tanggal >= DATE_SUB(NOW(), INTERVAL 7 DAY) ORDER BY tanggal DESC LIMIT %s",
                (limit,)
            )
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get latest pengumuman error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def create(judul, isi):
        """
        Membuat pengumuman baru.
        Returns: id_pengumuman baru, atau None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO pengumuman (judul, isi) VALUES (%s, %s)"
            cursor.execute(query, (judul, isi))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            logger.error(f"Create pengumuman error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def delete(id_pengumuman):
        """Menghapus pengumuman."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pengumuman WHERE id_pengumuman = %s", (id_pengumuman,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Delete pengumuman error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def count():
        """Menghitung total pengumuman."""
        conn = get_db_connection()
        if not conn:
            return 0

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pengumuman")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Count pengumuman error: {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def update(id_pengumuman, judul, isi):
        """Mengupdate judul dan isi pengumuman."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE pengumuman SET judul = %s, isi = %s WHERE id_pengumuman = %s",
                (judul, isi, id_pengumuman)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Update pengumuman error: {e}")
            return False
        finally:
            conn.close()
