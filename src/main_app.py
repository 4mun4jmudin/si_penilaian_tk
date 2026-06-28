# pyrefly: ignore [missing-import]
from kivymd.app import MDApp
# pyrefly: ignore [missing-import]
from kivy.lang import Builder
# pyrefly: ignore [missing-import]
from kivy.uix.screenmanager import ScreenManager, Screen
# pyrefly: ignore [missing-import]
from kivy.clock import Clock
# pyrefly: ignore [missing-import]
from kivy.core.window import Window
# pyrefly: ignore [missing-import]
from kivy.storage.jsonstore import JsonStore
# pyrefly: ignore [missing-import]
from kivymd.uix.label import MDLabel
# pyrefly: ignore [missing-import]
from kivymd.uix.card import MDCard

# --- KV LANGUAGE (Desain UI) ---
# Kita menaruh desain UI di dalam string ini agar rapi dan terpusat
KV = '''
ScreenManager:
    SplashScreen:
    OnboardingScreen:
    LoginScreen:
    DashboardGuru:

<SplashScreen>:
    name: 'splash'
    md_bg_color: 1, 1, 1, 1  # Putih
    
    MDFloatLayout:
        # Logo atau Ikon Aplikasi
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

<OnboardingScreen>:
    name: 'onboarding'
    md_bg_color: 1, 1, 1, 1

    MDFloatLayout:
        # Carousel untuk slide geser
        MDCarousel:
            id: carousel
            direction: 'right'
            on_slide_complete: root.on_slide_change(self)

            # --- SLIDE 1 ---
            MDFloatLayout:
                Image:
                    source: "assets/images/onboard1.png" # Ganti dengan gambar/ikon
                    pos_hint: {"center_x": .5, "center_y": .6}
                    size_hint: .5, .5
                MDIcon:
                    icon: "notebook-edit"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    font_size: "100sp"
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.6, 0.8, 1
                MDLabel:
                    text: "Pencatatan Mudah"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    halign: "center"
                    font_style: "H4"
                    bold: True
                MDLabel:
                    text: "Input nilai perkembangan anak secara digital,\\ncepat, dan terorganisir."
                    pos_hint: {"center_x": .5, "center_y": .3}
                    halign: "center"
                    font_style: "Body1"
                    color: 0.5, 0.5, 0.5, 1

            # --- SLIDE 2 ---
            MDFloatLayout:
                MDIcon:
                    icon: "chart-bar"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    font_size: "100sp"
                    theme_text_color: "Custom"
                    text_color: 0.8, 0.4, 0.2, 1
                MDLabel:
                    text: "Analisa Otomatis"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    halign: "center"
                    font_style: "H4"
                    bold: True
                MDLabel:
                    text: "Algoritma Rule-Based mengolah nilai harian\\nmenjadi status perkembangan (BSB, BSH) instan."
                    pos_hint: {"center_x": .5, "center_y": .3}
                    halign: "center"
                    font_style: "Body1"
                    color: 0.5, 0.5, 0.5, 1

            # --- SLIDE 3 ---
            MDFloatLayout:
                MDIcon:
                    icon: "file-document-outline"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    font_size: "100sp"
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.8, 0.4, 1
                MDLabel:
                    text: "Laporan Real-time"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    halign: "center"
                    font_style: "H4"
                    bold: True
                MDLabel:
                    text: "Pantau hasil belajar dan unduh laporan\\nperkembangan anak kapan saja."
                    pos_hint: {"center_x": .5, "center_y": .3}
                    halign: "center"
                    font_style: "Body1"
                    color: 0.5, 0.5, 0.5, 1

        # Indikator Dots (Titik-titik slide)
        MDBoxLayout:
            pos_hint: {"center_x": .5, "center_y": .18}
            size_hint: .2, .05
            spacing: "10dp"
            halign: "center"
            
            MDIcon:
                id: dot1
                icon: "circle"
                font_size: "10sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
            MDIcon:
                id: dot2
                icon: "circle-outline"
                font_size: "10sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
            MDIcon:
                id: dot3
                icon: "circle-outline"
                font_size: "10sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1

        # Tombol Navigasi
        MDFillRoundFlatButton:
            id: btn_next
            text: "LANJUT"
            pos_hint: {"right": .9, "y": .05}
            on_release: root.next_slide()
            md_bg_color: 0, 0.5, 0, 1

        MDTextButton:
            text: "LEWATI"
            pos_hint: {"x": .1, "y": .065}
            theme_text_color: "Custom"
            text_color: 0.5, 0.5, 0.5, 1
            on_release: root.skip_onboarding()

<LoginScreen>:
    name: 'login'
    md_bg_color: 1, 1, 1, 1
    
    MDFloatLayout:
        # Header / Logo Kecil
        MDIcon:
            icon: "school"
            pos_hint: {"center_x": .5, "center_y": .85}
            font_size: "60sp"
            theme_text_color: "Custom"
            text_color: 0, 0.5, 0, 1

        MDLabel:
            text: "Selamat Datang"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .75}
            font_style: "H5"
            bold: True
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 0.8

        MDLabel:
            text: "Silakan masuk untuk melanjutkan"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .70}
            font_style: "Caption"
            theme_text_color: "Hint"

        # --- FORM INPUT ---
        MDTextField:
            id: user_field
            hint_text: "Username / NIP"
            icon_right: "account"
            icon_right_color: 0, 0.5, 0, 1
            mode: "rectangle"
            pos_hint: {"center_x": .5, "center_y": .58}
            size_hint_x: .85
            line_color_focus: 0, 0.5, 0, 1

        MDTextField:
            id: pass_field
            hint_text: "Password"
            icon_right: "eye-off"
            icon_right_color: 0, 0.5, 0, 1
            mode: "rectangle"
            pos_hint: {"center_x": .5, "center_y": .46}
            size_hint_x: .85
            password: True
            line_color_focus: 0, 0.5, 0, 1
            on_icon_right: root.show_password()

        # Tombol Lupa Password (Optional UX)
        MDTextButton:
            text: "Lupa Password?"
            pos_hint: {"right": .92, "center_y": .38}
            font_size: "12sp"
            theme_text_color: "Hint"

        # --- TOMBOL LOGIN UTAMA ---
        MDFillRoundFlatButton:
            text: "MASUK"
            pos_hint: {"center_x": .5, "center_y": .28}
            size_hint_x: .85
            md_bg_color: 0, 0.5, 0, 1
            font_size: "18sp"
            on_release: root.do_login()

        # Divider
        MDLabel:
            text: "atau"
            halign: "center"
            pos_hint: {"center_y": .20}
            font_style: "Caption"
            theme_text_color: "Hint"

        MDTextButton:
            text: "Login Sebagai Orang Tua"
            pos_hint: {"center_x": .5, "center_y": .15}
            theme_text_color: "Custom"
            text_color: 0, 0.5, 0, 1
            bold: True
            on_release: root.login_as_parent()

<DashboardGuru>:
    name: 'dashboard_guru'
    md_bg_color: 0.96, 0.96, 0.96, 1  # Abu-abu sangat muda (off-white)
    
    MDBoxLayout:
        orientation: 'vertical'
        
        # --- TOP BAR ---
        MDTopAppBar:
            title: "Dashboard Guru"
            elevation: 0
            pos_hint: {"top": 1}
            md_bg_color: 0, 0.5, 0, 1
            specific_text_color: 1, 1, 1, 1
            right_action_items: [["logout", lambda x: root.logout()]]

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "20dp"
                adaptive_height: True

                # --- PROFILE HEADER ---
                MDCard:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "100dp"
                    padding: "15dp"
                    radius: [15]
                    md_bg_color: 1, 1, 1, 1
                    elevation: 1
                    
                    MDIcon:
                        icon: "account-circle"
                        font_size: "60sp"
                        theme_text_color: "Custom"
                        text_color: 0, 0.5, 0, 1
                        pos_hint: {"center_y": .5}
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: ["15dp", "10dp", "0dp", "10dp"]
                        
                        MDLabel:
                            text: "Selamat Datang,"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                        
                        MDLabel:
                            id: label_nama_guru
                            text: "Ibu Guru Bunga" 
                            font_style: "H6"
                            bold: True
                            theme_text_color: "Primary"
                        
                        MDLabel:
                            text: "Wali Kelas: TK-A"
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1

                # --- QUICK STATS (RINGKASAN) ---
                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "80dp"
                    spacing: "15dp"

                    # Stat 1: Jumlah Siswa
                    MDCard:
                        radius: [10]
                        md_bg_color: 0.9, 0.95, 0.9, 1 # Hijau muda sekali
                        elevation: 0
                        padding: "10dp"
                        orientation: "vertical"
                        
                        MDLabel:
                            text: "Total Siswa"
                            font_style: "Caption"
                            halign: "center"
                        MDLabel:
                            text: "15" # Nanti dari DB
                            font_style: "H5"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1

                    # Stat 2: Semester
                    MDCard:
                        radius: [10]
                        md_bg_color: 0.9, 0.95, 0.9, 1
                        elevation: 0
                        padding: "10dp"
                        orientation: "vertical"
                        
                        MDLabel:
                            text: "Semester Aktif"
                            font_style: "Caption"
                            halign: "center"
                        MDLabel:
                            text: "Ganjil 24/25" 
                            font_style: "Subtitle1"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1

                MDLabel:
                    text: "Menu Utama"
                    font_style: "Subtitle1"
                    bold: True
                    theme_text_color: "Primary"
                    size_hint_y: None
                    height: "30dp"

                # --- MENU GRID ---
                GridLayout:
                    cols: 2
                    spacing: "15dp"
                    size_hint_y: None
                    height: "160dp" # Tinggi grid

                    # CARD MENU 1: INPUT NILAI
                    MDCard:
                        orientation: "vertical"
                        padding: "15dp"
                        radius: [15]
                        elevation: 2
                        ripple_behavior: True
                        on_release: root.go_to_input_nilai()
                        
                        MDIcon:
                            icon: "notebook-edit"
                            halign: "center"
                            font_size: "40sp"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1
                        
                        MDLabel:
                            text: "Input Penilaian"
                            halign: "center"
                            bold: True
                            font_style: "Subtitle2"
                        
                        MDLabel:
                            text: "Catat nilai harian"
                            halign: "center"
                            font_style: "Caption"
                            theme_text_color: "Secondary"

                    # CARD MENU 2: LAPORAN
                    MDCard:
                        orientation: "vertical"
                        padding: "15dp"
                        radius: [15]
                        elevation: 2
                        ripple_behavior: True
                        on_release: root.go_to_laporan()

                        MDIcon:
                            icon: "file-document-outline"
                            halign: "center"
                            font_size: "40sp"
                            theme_text_color: "Custom"
                            text_color: 0.8, 0.4, 0, 1
                        
                        MDLabel:
                            text: "Laporan Belajar"
                            halign: "center"
                            bold: True
                            font_style: "Subtitle2"
                        
                        MDLabel:
                            text: "Lihat hasil rekap"
                            halign: "center"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
'''

# --- LOGIC PYTHON ---

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
                self.manager.current = 'login'
            else:
                self.manager.current = 'onboarding'
        else:
            self.manager.current = 'onboarding'

class OnboardingScreen(Screen):
    def next_slide(self):
        carousel = self.ids.carousel
        current_slide = carousel.index
        if current_slide < 2:
            carousel.load_slide(carousel.slides[current_slide + 1])
        else:
            self.finish_onboarding()

    def skip_onboarding(self):
        self.finish_onboarding()

    def finish_onboarding(self):
        import os
        from kivy.app import App
        
        app = App.get_running_app()
        if app is not None:
            data_dir = app.user_data_dir
            path_json = os.path.join(data_dir, 'app_config.json')
            store = JsonStore(path_json)
            store.put('onboarding', completed=True)
            
        self.manager.transition.direction = 'left'
        self.manager.current = 'login'

    def on_slide_change(self, carousel_instance):
        index = carousel_instance.index
        self.ids.dot1.icon = "circle-outline"
        self.ids.dot2.icon = "circle-outline"
        self.ids.dot3.icon = "circle-outline"
        
        if index == 0:
            self.ids.dot1.icon = "circle"
            self.ids.btn_next.text = "LANJUT"
        elif index == 1:
            self.ids.dot2.icon = "circle"
            self.ids.btn_next.text = "LANJUT"
        elif index == 2:
            self.ids.dot3.icon = "circle"
            self.ids.btn_next.text = "MULAI SEKARANG"

class LoginScreen(Screen):
    password_visible = False

    def show_password(self):
        field = self.ids.pass_field
        if self.password_visible:
            field.password = True
            field.icon_right = "eye-off"
            self.password_visible = False
        else:
            field.password = False
            field.icon_right = "eye"
            self.password_visible = True

    def do_login(self):
        username = self.ids.user_field.text
        password = self.ids.pass_field.text
        print(f"Mencoba login dengan User: {username}, Pass: {password}")
        
        # --- SIMULASI LOGIN BERHASIL ---
        if username and password:
            print("Login Berhasil! Masuk ke Dashboard Guru.")
            self.ids.user_field.text = ""
            self.ids.pass_field.text = ""
            self.manager.transition.direction = 'up'
            self.manager.current = 'dashboard_guru'
        else:
            print("Username/Password kosong")
        
    def login_as_parent(self):
        print("Beralih ke Login Orang Tua")

class DashboardGuru(Screen):
    def logout(self):
        print("Logout...")
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'

    def go_to_input_nilai(self):
        print("Navigasi ke Halaman Input Nilai")
        # Nanti: self.manager.current = 'input_nilai_screen'

    def go_to_laporan(self):
        print("Navigasi ke Halaman Laporan")
        # Nanti: self.manager.current = 'laporan_screen'

class TKPenilaianApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        if Window:
            Window.size = (360, 640) 
        return Builder.load_string(KV)

if __name__ == '__main__':
    TKPenilaianApp().run()