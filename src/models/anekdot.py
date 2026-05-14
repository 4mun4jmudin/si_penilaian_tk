"""
Model: Catatan Anekdot — Jurnal Harian Guru
=============================================
Menangani operasi CRUD untuk tabel `catatan_anekdot`.
"""

import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)


class AnekdotModel:

    @staticmethod
    def get_all(limit=50):
        """
        Mengambil semua catatan anekdot beserta nama siswa (JOIN).
        Urut dari terbaru.
        """
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT a.id_anekdot, a.tanggal, a.catatan, s.nama
                FROM catatan_anekdot a
                JOIN siswa s ON a.id_siswa = s.id_siswa
                ORDER BY a.tanggal DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get all anekdot error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def create(id_siswa, id_guru, tanggal, catatan):
        """
        Membuat catatan anekdot baru.
        Returns: id_anekdot baru, atau None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO catatan_anekdot (id_siswa, id_guru, tanggal, catatan) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (id_siswa, id_guru, tanggal, catatan))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            logger.error(f"Create anekdot error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_siswa(id_siswa):
        """Mengambil semua catatan anekdot untuk siswa tertentu."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT a.*, g.nama as nama_guru
                FROM catatan_anekdot a
                LEFT JOIN guru g ON a.id_guru = g.id_guru
                WHERE a.id_siswa = %s
                ORDER BY a.tanggal DESC
            """
            cursor.execute(query, (id_siswa,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get anekdot by siswa error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def delete(id_anekdot):
        """Menghapus catatan anekdot."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM catatan_anekdot WHERE id_anekdot = %s", (id_anekdot,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Delete anekdot error: {e}")
            return False
        finally:
            conn.close()
