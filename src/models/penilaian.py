"""
Model: Penilaian — Input & Rekap Nilai Harian
===============================================
Menangani operasi CRUD untuk tabel `penilaian`.
"""

import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)


class PenilaianModel:

    @staticmethod
    def create(id_siswa, id_guru, tgl, indikator, nilai, catatan=None):
        """
        Menyimpan satu data penilaian harian.
        Returns: id_penilaian baru, atau None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO penilaian (id_siswa, id_guru, tgl, indikator, nilai, catatan)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_siswa, id_guru, tgl, indikator, nilai, catatan))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            logger.error(f"Create penilaian error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_siswa(id_siswa):
        """Mengambil semua data penilaian untuk satu siswa."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM penilaian WHERE id_siswa = %s ORDER BY tgl DESC",
                (id_siswa,)
            )
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get penilaian by siswa error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_nilai_list_by_siswa(id_siswa):
        """
        Mengambil daftar nilai (angka saja) untuk satu siswa.
        Digunakan oleh algoritma Rule-Based.
        Returns: list[int], contoh: [4, 3, 4, 2, ...]
        """
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nilai FROM penilaian WHERE id_siswa = %s",
                (id_siswa,)
            )
            results = cursor.fetchall()
            return [row[0] for row in results]
        except Exception as e:
            logger.error(f"Get nilai list error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_all_with_filter(search_query=""):
        """Mengambil data penilaian dengan filter nama siswa atau indikator."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.*, s.nama as nama_siswa, s.kelas
                FROM penilaian p
                JOIN siswa s ON p.id_siswa = s.id_siswa
                WHERE s.nama LIKE %s OR p.indikator LIKE %s
                ORDER BY p.tgl DESC
            """
            like_val = f"%{search_query}%"
            cursor.execute(query, (like_val, like_val))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get all with filter error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def count():
        """Menghitung total penilaian yang sudah diinput."""
        conn = get_db_connection()
        if not conn:
            return 0

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM penilaian")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Count penilaian error: {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def count_today():
        """Menghitung jumlah penilaian hari ini."""
        conn = get_db_connection()
        if not conn:
            return 0

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM penilaian WHERE DATE(tgl) = CURDATE()")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Count penilaian today error: {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def get_details_by_siswa(id_siswa):
        """Mengambil seluruh detail penilaian (tgl, indikator, nilai, catatan) untuk seorang siswa."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT tgl, indikator, nilai, catatan
                FROM penilaian
                WHERE id_siswa = %s
                ORDER BY tgl DESC
            """
            cursor.execute(query, (id_siswa,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get details by siswa error: {e}")
            return []
        finally:
            conn.close()
