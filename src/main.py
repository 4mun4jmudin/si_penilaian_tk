# pyrefly: ignore [missing-import]
from kivymd.app import MDApp
# pyrefly: ignore [missing-import]
from kivy.core.window import Window
# pyrefly: ignore [missing-import]
from kivy.uix.screenmanager import ScreenManager

# --- 1. Import View Umum (Auth & Intro) ---
from views.splash_screen import SplashScreen
from views.onboarding_screen import OnboardingScreen
from views.auth.login_screen import LoginScreen

# --- 2. Import View Modul Guru ---
from views.guru.dashboard_guru import DashboardGuru
from views.guru.pilih_siswa import PilihSiswaScreen
from views.guru.input_nilai import InputNilaiScreen
from views.guru.generate_laporan import GenerateLaporanScreen
from views.guru.preview_laporan import PreviewLaporanScreen
from views.guru.data_siswa import DataSiswaScreen
from views.guru.catatan_anekdot import CatatanAnekdotScreen
from views.guru.riwayat_penilaian import RiwayatPenilaianScreen
from views.guru.profil_guru import ProfilGuruScreen
from views.guru.edit_profil_guru import EditProfilGuruScreen

# --- 3. Import View Modul Admin ---
from views.admin.dashboard_admin import DashboardAdmin
from views.admin.kelola_guru import KelolaGuruScreen
from views.admin.kelola_siswa import KelolaSiswaScreen
from views.admin.kelola_pengumuman import KelolaPengumumanScreen
from views.admin.profil_admin import ProfilAdminScreen

# --- 4. Import View Modul Orang Tua ---
from views.orangtua.dashboard_ortu import DashboardOrtu
from views.orangtua.history_laporan import HistoryLaporanScreen
from views.orangtua.detail_laporan_ortu import DetailLaporanOrtuScreen
from views.orangtua.profil_ortu import ProfilOrtuScreen
from views.orangtua.edit_profil_ortu import EditProfilOrtuScreen
from views.orangtua.perkembangan_anak_ortu import PerkembanganAnakOrtuScreen

class TKPenilaianApp(MDApp):
    def build(self):
        # Konfigurasi Tema Dasar
        self.theme_cls.primary_palette = "Green"  # Warna dasar aplikasi
        self.theme_cls.theme_style = "Light"      # Mode terang
        
        # Ukuran Window simulasi HP (Hapus baris ini saat deploy ke Android asli)
        # pyrefly: ignore [missing-attribute]
        Window.size = (360, 640) 
        
        # Inisialisasi Screen Manager
        sm = ScreenManager()
        
        # --- MENDAFTARKAN SEMUA SCREEN ---
        
        # 1. Alur Awal
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(LoginScreen(name='login'))
        
        # 2. Modul Guru
        sm.add_widget(DashboardGuru(name='dashboard_guru'))
        sm.add_widget(PilihSiswaScreen(name='pilih_siswa'))
        sm.add_widget(InputNilaiScreen(name='input_nilai'))
        sm.add_widget(GenerateLaporanScreen(name='generate_laporan'))
        sm.add_widget(PreviewLaporanScreen(name='preview_laporan'))
        sm.add_widget(DataSiswaScreen(name='data_siswa'))
        sm.add_widget(CatatanAnekdotScreen(name='catatan_anekdot'))
        sm.add_widget(RiwayatPenilaianScreen(name='riwayat_penilaian'))
        sm.add_widget(ProfilGuruScreen(name='profil_guru'))
        sm.add_widget(EditProfilGuruScreen(name='edit_profil_guru'))
        
        # 3. Modul Admin
        sm.add_widget(DashboardAdmin(name='dashboard_admin'))
        sm.add_widget(KelolaGuruScreen(name='kelola_guru'))
        sm.add_widget(KelolaSiswaScreen(name='kelola_siswa'))
        sm.add_widget(KelolaPengumumanScreen(name='kelola_pengumuman'))
        sm.add_widget(ProfilAdminScreen(name='profil_admin'))
        
        # 4. Modul Orang Tua
        sm.add_widget(DashboardOrtu(name='dashboard_ortu'))
        sm.add_widget(HistoryLaporanScreen(name='history_laporan'))
        sm.add_widget(DetailLaporanOrtuScreen(name='detail_laporan_ortu'))
        sm.add_widget(ProfilOrtuScreen(name='profil_ortu'))
        sm.add_widget(EditProfilOrtuScreen(name='edit_profil_ortu'))
        sm.add_widget(PerkembanganAnakOrtuScreen(name='perkembangan_anak_ortu'))
        
        return sm

if __name__ == '__main__':
    TKPenilaianApp().run()