"""
Model: Guru — Manajemen Data Guru
===================================
Menangani operasi CRUD untuk tabel `guru`.
"""

import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)


class GuruModel:

    @staticmethod
    def get_all():
        """Mengambil semua data guru beserta username (JOIN), urut abjad."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT g.*, u.username 
                FROM guru g
                JOIN users u ON g.id_user = u.id
                ORDER BY g.nama ASC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get all guru error: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_user_id(id_user):
        """Mengambil data guru berdasarkan id_user (foreign key ke tabel users)."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM guru WHERE id_user = %s", (id_user,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get guru by user_id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_guru):
        """Mengambil data guru berdasarkan id_guru."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM guru WHERE id_guru = %s", (id_guru,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get guru by id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def create(id_user, nama, nip):
        """
        Membuat data guru baru (setelah user sudah dibuat).
        Returns: id_guru baru, atau None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO guru (id_user, nama, nip) VALUES (%s, %s, %s)"
            cursor.execute(query, (id_user, nama, nip))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            logger.error(f"Create guru error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id_guru, nama, nip, no_hp=None, foto=None):
        """Update profil guru (nama, NIP, no_hp, dan foto)."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            # Gunakan query dinamis agar tidak menimpa data no_hp/foto jika tidak dikirim
            query = "UPDATE guru SET nama=%s, nip=%s"
            params = [nama, nip]
            
            if no_hp is not None:
                query += ", no_hp=%s"
                params.append(no_hp)
            if foto is not None:
                query += ", foto=%s"
                params.append(foto)
                
            query += " WHERE id_guru=%s"
            params.append(id_guru)
            
            cursor.execute(query, tuple(params))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Update guru error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def count():
        """Menghitung total guru terdaftar."""
        conn = get_db_connection()
        if not conn:
            return 0

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM guru")
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Count guru error: {e}")
            return 0
        finally:
            conn.close()
