import sys
sys.path.append('src')
from config.database import get_db_connection

conn = get_db_connection()
c = conn.cursor(dictionary=True)

c.execute('SELECT id_siswa, nama, id_user_ortu FROM siswa')
rows = c.fetchall()
print('=== DATA SISWA ===')
for r in rows:
    print(r)

c.execute("SELECT id, username, role FROM users WHERE role='OrangTua'")
users = c.fetchall()
print('=== AKUN ORTU ===')
for u in users:
    print(u)

conn.close()
