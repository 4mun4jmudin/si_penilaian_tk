"""
Model: User — Autentikasi & Manajemen Akun
============================================
Menangani operasi CRUD untuk tabel `users`.
"""

import logging
from config.database import get_db_connection

logger = logging.getLogger(__name__)


class UserModel:

    @staticmethod
    def authenticate(username, password):
        """
        Validasi kredensial login (bisa menggunakan username atau NIP untuk guru).
        Returns: dict user data jika valid, None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            
            # 1. Coba login dengan username biasa
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                return user
            
            # 2. Coba login dengan NIP (jika user tidak ditemukan dengan username)
            # JOIN dengan tabel guru untuk cek NIP
            query_nip = """
                SELECT u.* FROM users u
                JOIN guru g ON u.id = g.id_user
                WHERE g.nip = %s AND u.password = %s
            """
            cursor.execute(query_nip, (username, password))
            user_by_nip = cursor.fetchone()
            
            return user_by_nip
            
        except Exception as e:
            logger.error(f"Authenticate error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_user):
        """Mengambil data user berdasarkan ID."""
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (id_user,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Get user by id error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def create(username, password, role='Guru'):
        """
        Membuat user baru.
        Returns: id user yang baru dibuat, atau None jika gagal.
        """
        conn = get_db_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, role))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            logger.error(f"Create user error: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update_username(id_user, new_username):
        """Update username saja."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username=%s WHERE id=%s", (new_username, id_user))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Update username error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def update_credentials(id_user, username, password):
        """Update username dan password."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET username=%s, password=%s WHERE id=%s",
                (username, password, id_user)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Update credentials error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id_user):
        """Menghapus user (CASCADE akan menghapus guru terkait)."""
        conn = get_db_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (id_user,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Delete user error: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_by_role(role):
        """Mengambil daftar user berdasarkan role."""
        conn = get_db_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, role FROM users WHERE role = %s ORDER BY username ASC", (role,))
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Get users by role error: {e}")
            return []
        finally:
            conn.close()
