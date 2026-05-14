"""
Model: Laporan — Generate & Riwayat Laporan
=============================================
Menangani operasi CRUD untuk tabel `laporan`.
"""

import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)


class LaporanModel:

    @staticmethod
    def create(id_siswa, periode, hasil):
        """
        Membuat laporan baru (hasil generate rule-based).
        Returns: id_laporan baru, atau None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO laporan (id_siswa, periode, hasil) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_siswa, periode, hasil))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            logger.error(f"Create laporan error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_laporan):
        """
        Mengambil detail laporan beserta data siswa (JOIN).
        Returns: dict dengan key: periode, hasil, nama_siswa, kelas
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT
                    l.id_laporan,
                    l.periode,
                    l.hasil,
                    l.created_at,
                    s.nama AS nama_siswa,
                    s.kelas
                FROM laporan l
                JOIN siswa s ON l.id_siswa = s.id_siswa
                WHERE l.id_laporan = %s
            """
            cursor.execute(query, (id_laporan,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get laporan by id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_siswa(id_siswa):
        """Mengambil semua laporan untuk satu siswa (riwayat)."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT id_laporan, periode, created_at
                FROM laporan
                WHERE id_siswa = %s
                ORDER BY id_laporan DESC
            """
            cursor.execute(query, (id_siswa,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get laporan by siswa error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_latest_periode():
        """Mengambil periode terbaru dari laporan manapun."""
        conn = get_db_connection()
        if not conn:
            return "Ganjil 2025"

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT periode FROM laporan ORDER BY id_laporan DESC LIMIT 1")
            result = cursor.fetchone()
            return result[0] if result else "Ganjil 2025"
        except Exception as e:
            logger.error(f"Get latest periode error: {e}")
            return "Ganjil 2025"
        finally:
            conn.close()

    @staticmethod
    def count_by_siswa(id_siswa):
        """Menghitung jumlah laporan untuk satu siswa."""
        conn = get_db_connection()
        if not conn:
            return 0

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM laporan WHERE id_siswa = %s",
                (id_siswa,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Count laporan error: {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def get_latest_periode_by_siswa(id_siswa):
        """Mengambil periode terbaru untuk satu siswa."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT periode FROM laporan WHERE id_siswa = %s ORDER BY id_laporan DESC LIMIT 1",
                (id_siswa,)
            )
            result = cursor.fetchone()
            return result['periode'] if result else None
        except Exception as e:
            logger.error(f"Get latest periode by siswa error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def count():
        """Menghitung total laporan yang sudah di-generate."""
        conn = get_db_connection()
        if not conn:
            return 0

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM laporan")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Count laporan error: {e}")
            return 0
        finally:
            conn.close()
