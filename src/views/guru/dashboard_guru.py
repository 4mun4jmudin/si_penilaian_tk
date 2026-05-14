# pyrefly: ignore [missing-import]
from kivy.lang import Builder
# pyrefly: ignore [missing-import]
from kivy.uix.screenmanager import Screen
# pyrefly: ignore [missing-import]
from kivy.uix.behaviors import ButtonBehavior
# pyrefly: ignore [missing-import]
from kivy.animation import Animation
# pyrefly: ignore [missing-import]
from kivy.properties import StringProperty, ListProperty
# pyrefly: ignore [missing-import]
from kivymd.uix.boxlayout import MDBoxLayout
# pyrefly: ignore [missing-import]
from kivymd.uix.card import MDCard
# pyrefly: ignore [missing-import]
from kivymd.toast import toast
# Import Model Layer (MVC) & Session
from config.session import current_user, clear_session
from models.siswa import SiswaModel
from models.laporan import LaporanModel

# =====================================================================
# CUSTOM WIDGET: Animated Menu Card dengan Hover & Press Effect
# =====================================================================
class MenuCard(MDCard):
    """Card menu dengan efek animasi hover (desktop) dan press."""

    _original_elevation = 2
    _original_scale = 1.0

    def on_enter(self):
        """Mouse masuk area card (hover) - desktop only."""
        anim = Animation(elevation=6, duration=0.15)
        anim.start(self)

    def on_leave(self):
        """Mouse keluar area card."""
        anim = Animation(elevation=self._original_elevation, duration=0.15)
        anim.start(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            anim = Animation(elevation=1, duration=0.08)
            anim.start(self)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            anim = Animation(elevation=self._original_elevation, duration=0.12)
            anim.start(self)
        return super().on_touch_up(touch)


# =====================================================================
# KV LANGUAGE - PREMIUM MODERN DASHBOARD 2026
# =====================================================================
KV = '''
#:import Animation kivy.animation.Animation

# --- COLOR PALETTE (Hijau Elegan Islami) ---
# Primary Green    : 0.13, 0.55, 0.33, 1   (#22 8C 54)
# Dark Green       : 0.08, 0.40, 0.24, 1   (#14 66 3D)
# Light Green Tint : 0.93, 0.98, 0.95, 1   (#ED FA F2)
# Surface White    : 1, 1, 1, 1
# Background       : 0.965, 0.973, 0.980, 1  (#F7 F8 FA)
# Text Primary     : 0.12, 0.14, 0.17, 1
# Text Secondary   : 0.45, 0.50, 0.56, 1
# Accent Gold      : 0.85, 0.65, 0.13, 1   (Islamic gold)
# Icon Bg Mint     : 0.85, 0.95, 0.90, 1
# Icon Bg Gold     : 1.0, 0.95, 0.85, 1
# Icon Bg Blue     : 0.88, 0.93, 1.0, 1
# Icon Bg Rose     : 1.0, 0.91, 0.93, 1

# ======= MENU CARD TEMPLATE =======
<MenuCard>:
    orientation: "vertical"
    radius: [18]
    elevation: 2
    md_bg_color: 1, 1, 1, 1
    ripple_behavior: True
    padding: "18dp"
    spacing: "8dp"

# ======= MAIN DASHBOARD LAYOUT =======
<DashboardGuru>:
    name: 'dashboard_guru'
    md_bg_color: 0.965, 0.973, 0.980, 1

    MDBoxLayout:
        orientation: 'vertical'

        # ===== TOP HEADER BAR =====
        # Gradient-style header hijau elegan dengan shadow
        MDCard:
            size_hint_y: None
            height: "64dp"
            radius: [0, 0, 0, 0]
            elevation: 3
            md_bg_color: 0.13, 0.55, 0.33, 1
            padding: ["20dp", "0dp", "12dp", "0dp"]
            ripple_behavior: False

            MDBoxLayout:
                orientation: "horizontal"
                pos_hint: {"center_y": .5}

                # Icon Sekolah
                MDIcon:
                    icon: "mosque"
                    font_size: "26sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.9
                    size_hint_x: None
                    width: "36dp"
                    pos_hint: {"center_y": .5}

                # Nama Sekolah
                MDBoxLayout:
                    orientation: "vertical"
                    padding: ["10dp", "0dp", "0dp", "0dp"]
                    pos_hint: {"center_y": .5}

                    MDLabel:
                        text: "TK Miftahul Jannah"
                        font_style: "H6"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1

                    MDLabel:
                        text: "Sistem Penilaian Digital"
                        font_style: "Overline"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.65

                # Tombol Profil
                MDIconButton:
                    icon: "account-circle"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.85
                    pos_hint: {"center_y": .5}
                    on_release: root.go_to_profil()


        # ===== SCROLLABLE CONTENT =====
        ScrollView:
            do_scroll_x: False
            bar_width: "3dp"
            bar_color: 0.13, 0.55, 0.33, 0.4

            MDBoxLayout:
                orientation: 'vertical'
                padding: ["20dp", "24dp", "20dp", "30dp"]
                spacing: "20dp"
                adaptive_height: True


                # ===== 1. WELCOME CARD (Premium Gradient Feel) =====
                MDCard:
                    size_hint_y: None
                    height: "130dp"
                    radius: [22]
                    elevation: 4
                    md_bg_color: 0.13, 0.55, 0.33, 1
                    ripple_behavior: False
                    padding: ["24dp", "20dp", "12dp", "20dp"]

                    # Row: [Kiri = Text Column] [Kanan = Icon Ilustrasi]
                    MDBoxLayout:
                        orientation: "horizontal"

                        # === KIRI: Vertical Text Stack ===
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "3dp"
                            pos_hint: {"center_y": .5}

                            # Baris 1: Salam
                            MDLabel:
                                text: "Assalamu'alaikum,"
                                font_style: "Body2"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 0.7
                                size_hint_y: None
                                height: "22dp"
                                shorten: True
                                shorten_from: "right"
                                text_size: self.width, None

                            # Baris 2: Nama Guru
                            MDLabel:
                                id: label_nama_guru
                                text: "Memuat..."
                                font_style: "H5"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                size_hint_y: None
                                height: "36dp"
                                shorten: True
                                shorten_from: "right"
                                text_size: self.width, None

                            Widget:
                                size_hint_y: None
                                height: "4dp"

                            # Baris 3: Badge Posisi (horizontal row)
                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint_y: None
                                height: "26dp"
                                spacing: "6dp"
                                md_bg_color: 1, 1, 1, 0.18
                                radius: [13]
                                padding: ["10dp", "0dp", "14dp", "0dp"]
                                size_hint_x: None
                                width: "160dp"

                                MDIcon:
                                    icon: "shield-check"
                                    font_size: "14sp"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 0.9
                                    size_hint_x: None
                                    width: "20dp"
                                    pos_hint: {"center_y": .5}

                                MDLabel:
                                    id: label_nip
                                    text: "Pengajar"
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 0.9
                                    pos_hint: {"center_y": .5}
                                    shorten: True
                                    shorten_from: "right"
                                    text_size: self.width, None

                        # === KANAN: Icon Ilustrasi (fixed width) ===
                        MDBoxLayout:
                            size_hint_x: None
                            width: "80dp"

                            MDIcon:
                                icon: "book-open-page-variant-outline"
                                font_size: "68sp"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 0.15
                                halign: "center"
                                pos_hint: {"center_y": .5}


                # ===== 2. STATISTIK CARDS =====
                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "110dp"
                    spacing: "14dp"

                    # Card Siswa Aktif
                    MDCard:
                        radius: [18]
                        elevation: 2
                        md_bg_color: 1, 1, 1, 1
                        padding: "16dp"
                        orientation: "vertical"
                        ripple_behavior: True
                        on_release: root.toast_info("Total siswa aktif terdaftar")

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: "36dp"

                            # Icon Badge
                            MDBoxLayout:
                                size_hint: None, None
                                size: "36dp", "36dp"
                                md_bg_color: 0.85, 0.95, 0.90, 1
                                radius: [10]
                                pos_hint: {"center_y": .5}

                                MDIcon:
                                    icon: "account-group-outline"
                                    font_size: "20sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.13, 0.55, 0.33, 1
                                    halign: "center"
                                    pos_hint: {"center_y": .5}

                            Widget:

                            MDIcon:
                                icon: "trending-up"
                                font_size: "16sp"
                                theme_text_color: "Custom"
                                text_color: 0.13, 0.55, 0.33, 0.6
                                pos_hint: {"center_y": .5}
                                size_hint_x: None
                                width: "20dp"

                        Widget:
                            size_hint_y: None
                            height: "4dp"

                        MDLabel:
                            id: label_total_siswa
                            text: "0"
                            font_style: "H4"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1

                        MDLabel:
                            text: "Siswa Aktif"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1

                    # Card Periode
                    MDCard:
                        radius: [18]
                        elevation: 2
                        md_bg_color: 1, 1, 1, 1
                        padding: "16dp"
                        orientation: "vertical"
                        ripple_behavior: True
                        on_release: root.toast_info("Periode akademik berjalan")

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: "36dp"

                            # Icon Badge
                            MDBoxLayout:
                                size_hint: None, None
                                size: "36dp", "36dp"
                                md_bg_color: 1.0, 0.95, 0.85, 1
                                radius: [10]
                                pos_hint: {"center_y": .5}

                                MDIcon:
                                    icon: "calendar-month-outline"
                                    font_size: "20sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.85, 0.65, 0.13, 1
                                    halign: "center"
                                    pos_hint: {"center_y": .5}

                            Widget:

                            MDIcon:
                                icon: "clock-outline"
                                font_size: "16sp"
                                theme_text_color: "Custom"
                                text_color: 0.85, 0.65, 0.13, 0.6
                                pos_hint: {"center_y": .5}
                                size_hint_x: None
                                width: "20dp"

                        Widget:
                            size_hint_y: None
                            height: "4dp"

                        MDLabel:
                            id: label_semester
                            text: "-"
                            font_style: "H6"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1
                            shorten: True
                            shorten_from: 'right'

                        MDLabel:
                            text: "Periode"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1


                # ===== 3. SECTION TITLE: AKTIVITAS UTAMA =====
                MDBoxLayout:
                    size_hint_y: None
                    height: "28dp"
                    padding: ["2dp", "0dp", "0dp", "0dp"]

                    MDLabel:
                        text: "Aktivitas Utama"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.14, 0.17, 1


                # ===== 4. MENU GRID (2 Kolom, 4 Item) =====
                MDGridLayout:
                    cols: 2
                    spacing: "14dp"
                    adaptive_height: True

                    # --- MENU 1: Input Penilaian Harian ---
                    MenuCard:
                        size_hint_y: None
                        height: "145dp"
                        on_release: root.go_to_input_nilai()

                        # Icon Container
                        MDBoxLayout:
                            size_hint: None, None
                            size: "48dp", "48dp"
                            md_bg_color: 0.85, 0.95, 0.90, 1
                            radius: [14]

                            MDIcon:
                                icon: "clipboard-edit-outline"
                                font_size: "24sp"
                                theme_text_color: "Custom"
                                text_color: 0.13, 0.55, 0.33, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                        Widget:
                            size_hint_y: None
                            height: "6dp"

                        MDLabel:
                            text: "Input Penilaian"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Catat nilai harian"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                    # --- MENU 2: Jurnal Catatan Harian ---
                    MenuCard:
                        size_hint_y: None
                        height: "145dp"
                        on_release: root.go_to_catatan_anekdot()

                        MDBoxLayout:
                            size_hint: None, None
                            size: "48dp", "48dp"
                            md_bg_color: 1.0, 0.95, 0.85, 1
                            radius: [14]

                            MDIcon:
                                icon: "notebook-edit-outline"
                                font_size: "24sp"
                                theme_text_color: "Custom"
                                text_color: 0.85, 0.65, 0.13, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                        Widget:
                            size_hint_y: None
                            height: "6dp"

                        MDLabel:
                            text: "Catatan Anekdot"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Catatan anekdot"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                    # --- MENU 3: Laporan & Rekap ---
                    MenuCard:
                        size_hint_y: None
                        height: "145dp"
                        on_release: root.go_to_laporan()

                        MDBoxLayout:
                            size_hint: None, None
                            size: "48dp", "48dp"
                            md_bg_color: 0.88, 0.93, 1.0, 1
                            radius: [14]

                            MDIcon:
                                icon: "file-chart-outline"
                                font_size: "24sp"
                                theme_text_color: "Custom"
                                text_color: 0.25, 0.47, 0.85, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                        Widget:
                            size_hint_y: None
                            height: "6dp"

                        MDLabel:
                            text: "Laporan & Rekap"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Hasil evaluasi siswa"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                    # --- MENU 4: Data Siswa ---
                    MenuCard:
                        size_hint_y: None
                        height: "145dp"
                        on_release: root.go_to_data_siswa()

                        MDBoxLayout:
                            size_hint: None, None
                            size: "48dp", "48dp"
                            md_bg_color: 1.0, 0.91, 0.93, 1
                            radius: [14]

                            MDIcon:
                                icon: "account-school-outline"
                                font_size: "24sp"
                                theme_text_color: "Custom"
                                text_color: 0.85, 0.30, 0.40, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                        Widget:
                            size_hint_y: None
                            height: "6dp"

                        MDLabel:
                            text: "Data Siswa"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Manajemen data kelas"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                    # --- MENU 5: Riwayat Penilaian ---
                    MenuCard:
                        size_hint_y: None
                        height: "145dp"
                        on_release: root.go_to_riwayat_penilaian()

                        MDBoxLayout:
                            size_hint: None, None
                            size: "48dp", "48dp"
                            md_bg_color: 0.95, 0.85, 1.0, 1
                            radius: [14]

                            MDIcon:
                                icon: "history"
                                font_size: "24sp"
                                theme_text_color: "Custom"
                                text_color: 0.6, 0.2, 0.8, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                        Widget:
                            size_hint_y: None
                            height: "6dp"

                        MDLabel:
                            text: "Riwayat Penilaian"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Cari riwayat nilai siswa"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1
                            size_hint_y: None
                            height: self.texture_size[1]


                # ===== FOOTER BRANDING =====
                Widget:
                    size_hint_y: None
                    height: "20dp"

                MDLabel:
                    text: "TK Islam Plus Miftahul Jannah - v2.0"
                    font_style: "Overline"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.45, 0.50, 0.56, 0.5
                    size_hint_y: None
                    height: "20dp"
'''

Builder.load_string(KV)


# =====================================================================
# PYTHON LOGIC - DashboardGuru Screen
# =====================================================================
class DashboardGuru(Screen):

    def on_enter(self):
        self.load_user_data()
        self.load_dashboard_stats()

    def load_user_data(self):
        nama = current_user.get('nama_lengkap', 'Ibu/Bapak Guru')
        role = current_user.get('role', 'Pengajar')

        self.ids.label_nama_guru.text = nama
        self.ids.label_nip.text = f"Posisi: {role}"

    def load_dashboard_stats(self):
        """Memuat statistik dashboard menggunakan Model Layer."""
        # Hitung Total Siswa via Model
        total_siswa = SiswaModel.count()
        self.ids.label_total_siswa.text = str(total_siswa)

        # Ambil Periode Terakhir via Model
        periode = LaporanModel.get_latest_periode()
        self.ids.label_semester.text = str(periode)

    def toast_info(self, text):
        toast(text)

    def logout(self):
        clear_session()
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'

    def go_to_input_nilai(self):
        # Ke halaman pilih siswa sebelum input nilai
        self.manager.transition.direction = 'left'
        self.manager.current = 'pilih_siswa'

    def go_to_laporan(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'generate_laporan'

    def go_to_data_siswa(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'data_siswa'

    def go_to_riwayat_penilaian(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'riwayat_penilaian'

    def go_to_catatan_anekdot(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'catatan_anekdot'

    def go_to_profil(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'profil_guru'