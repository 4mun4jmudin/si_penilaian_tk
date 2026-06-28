import sys
import os

# Menambahkan folder src ke path agar import berjalan lancar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import aplikasi utama dari src/main.py
from src.main import TKPenilaianApp

if __name__ == '__main__':
    TKPenilaianApp().run()
