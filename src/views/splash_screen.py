from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

# Desain UI khusus Splash Screen
KV = '''
<SplashScreen>:
    name: 'splash'
    md_bg_color: 1, 1, 1, 1  # Putih
    
    MDFloatLayout:
        MDIcon:
            icon: "school"
            halign: "center"
            valign: "center"
            pos_hint: {"center_x": .5, "center_y": .55}
            font_size: "80sp"
            theme_text_color: "Custom"
            text_color: 0, 0.5, 0, 1  # Warna Hijau TK

        MDLabel:
            text: "TK Islam Plus\\nMiftahul Jannah"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .45}
            font_style: "H5"
            bold: True
            theme_text_color: "Custom"
            text_color: 0, 0.5, 0, 1
        
        MDLabel:
            text: "Sistem Penilaian & Laporan"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .38}
            font_style: "Caption"
'''

# Load string KV saat modul ini di-import
Builder.load_string(KV)

class SplashScreen(Screen):
    def on_enter(self, *args):
        # Timer: Pindah ke layar berikutnya setelah 3 detik
        self.timer = Clock.schedule_once(self.check_onboarding_status, 3)

    def on_leave(self, *args):
        # Batalkan timer jika pindah layar sebelum 3 detik
        if hasattr(self, 'timer'):
            self.timer.cancel()

    def check_onboarding_status(self, dt):
        # Cek penyimpanan lokal apakah user sudah pernah buka aplikasi
        import os
        from kivy.app import App
        
        app = App.get_running_app()
        if app is None:
            return  # Aplikasi sudah ditutup, batalkan proses
            
        data_dir = app.user_data_dir
        path_json = os.path.join(data_dir, 'app_config.json')
        store = JsonStore(path_json)
        
        if store.exists('onboarding'):
            if store.get('onboarding')['completed']:
                # Jika sudah pernah, langsung ke Login
                self.manager.current = 'login'
            else:
                self.manager.current = 'onboarding'
        else:
            # Jika belum ada data (pertama kali install), ke Onboarding
            self.manager.current = 'onboarding'