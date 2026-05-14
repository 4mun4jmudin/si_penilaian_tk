import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("UPDATE users SET password = 'password'")
conn.commit()
print("Done! Semua password dikembalikan ke plaintext 'password'.")

cursor.execute("SELECT id, username, password FROM users")
for row in cursor.fetchall():
    print(row)
conn.close()
