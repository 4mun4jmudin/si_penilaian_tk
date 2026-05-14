"""
Model: Siswa — Manajemen Data Siswa
=====================================
Menangani operasi CRUD untuk tabel `siswa`.
"""

import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)


class SiswaModel:

    @staticmethod
    def get_all():
        """Mengambil semua data siswa, urut abjad."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM siswa ORDER BY nama ASC")
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get all siswa error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_siswa):
        """Mengambil data satu siswa berdasarkan ID."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM siswa WHERE id_siswa = %s", (id_siswa,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get siswa by id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_first():
        """Mengambil data siswa pertama (untuk demo orang tua)."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM siswa LIMIT 1")
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get first siswa error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id_user_ortu(id_user_ortu):
        """Mengambil data siswa yang berelasi dengan id user ortu."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM siswa WHERE id_user_ortu = %s", (id_user_ortu,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get siswa by ortu id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def create(nama, kelas, nama_orang_tua, tanggal_lahir=None, id_user_ortu=None, alamat=None, jenis_kelamin=None):
        """
        Menambah siswa baru.
        Returns: id_siswa baru, atau None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO siswa (nama, kelas, nama_orang_tua, tanggal_lahir, id_user_ortu, alamat, jenis_kelamin) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (nama, kelas, nama_orang_tua, tanggal_lahir, id_user_ortu, alamat, jenis_kelamin))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            logger.error(f"Create siswa error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id_siswa, nama, kelas, nama_orang_tua, tanggal_lahir=None, alamat=None, jenis_kelamin=None, foto_anak=None, foto_ortu=None, no_hp_ortu=None, email_ortu=None):
        """Update data siswa lengkap."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "UPDATE siswa SET nama=%s, kelas=%s, nama_orang_tua=%s, tanggal_lahir=%s, alamat=%s, jenis_kelamin=%s, foto_anak=%s, foto_ortu=%s, no_hp_ortu=%s, email_ortu=%s WHERE id_siswa=%s"
            cursor.execute(query, (nama, kelas, nama_orang_tua, tanggal_lahir, alamat, jenis_kelamin, foto_anak, foto_ortu, no_hp_ortu, email_ortu, id_siswa))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Update siswa error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id_siswa):
        """Menghapus data siswa."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM siswa WHERE id_siswa = %s", (id_siswa,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Delete siswa error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def count():
        """Menghitung total siswa terdaftar."""
        conn = get_db_connection()
        if not conn:
            return 0

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM siswa")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Count siswa error: {e}")
            return 0
        finally:
            conn.close()

    @staticmethod
    def link_ortu(id_siswa, id_user_ortu):
        """Menghubungkan akun orang tua ke siswa."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            # Lepas dulu link lama jika ortu sudah terhubung ke siswa lain
            if id_user_ortu:
                cursor.execute("UPDATE siswa SET id_user_ortu = NULL WHERE id_user_ortu = %s", (id_user_ortu,))
            cursor.execute("UPDATE siswa SET id_user_ortu = %s WHERE id_siswa = %s", (id_user_ortu, id_siswa))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Link ortu error: {e}")
            return False
        finally:
            conn.close()
