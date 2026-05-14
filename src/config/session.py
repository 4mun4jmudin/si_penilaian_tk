"""
=================================================================
Session Manager — Sistem Penilaian TK Miftahul Jannah
=================================================================
Mengelola state user yang sedang login (in-memory session).
Digunakan oleh semua modul untuk mengetahui siapa yang aktif.

Version: 2.0 (Refactored)
=================================================================
"""

import logging

logger = logging.getLogger(__name__)

# ----- Data Session (In-Memory) -----
_current_user = {
    "id_user": None,
    "id_guru": None,       # Khusus role Guru
    "id_siswa": None,      # Khusus role OrangTua (siswa yang terhubung)
    "username": None,
    "role": None,           # 'Admin', 'Guru', 'OrangTua'
    "nama_lengkap": None,
}


def set_current_user(id_user, username, role, nama_lengkap=None, id_guru=None, id_siswa=None):
    """
    Menyimpan data user yang berhasil login ke session.
    Dipanggil setelah proses autentikasi berhasil.
    """
    _current_user["id_user"] = id_user
    _current_user["username"] = username
    _current_user["role"] = role
    _current_user["nama_lengkap"] = nama_lengkap
    _current_user["id_guru"] = id_guru
    _current_user["id_siswa"] = id_siswa
    logger.info(f"Session aktif: {username} (Role: {role})")


def get_current_user():
    """
    Mengembalikan salinan data user saat ini (read-only copy).
    Menggunakan copy agar Views tidak bisa mengubah session secara langsung.
    """
    return _current_user.copy()


def clear_session():
    """
    Menghapus semua data session (logout).
    """
    for key in _current_user:
        _current_user[key] = None
    logger.info("Session cleared (logout)")


# ----- Backward Compatibility -----
# Variabel `current_user` tetap dipertahankan agar kode lama
# yang menggunakan `from config.session import current_user`
# tidak langsung error. Secara bertahap migrasi ke get_current_user().
current_user = _current_user