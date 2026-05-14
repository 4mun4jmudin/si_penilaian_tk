# pyrefly: ignore [missing-import]
from kivy.lang import Builder
# pyrefly: ignore [missing-import]
from kivy.uix.screenmanager import Screen
# pyrefly: ignore [missing-import]
from kivy.animation import Animation
# pyrefly: ignore [missing-import]
from kivymd.uix.card import MDCard
# pyrefly: ignore [missing-import]
from kivymd.toast import toast
# pyrefly: ignore [missing-import]
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
# pyrefly: ignore [missing-import]
from kivy.metrics import dp

from config.session import current_user, clear_session
from models.guru import GuruModel
from models.siswa import SiswaModel
from models.penilaian import PenilaianModel
from models.laporan import LaporanModel
from models.pengumuman import PengumumanModel

# =====================================================================
# CUSTOM WIDGET: Animated Menu Card with Hover Effect
# =====================================================================
class AdminMenuCard(MDCard):
    """Card menu dengan efek animasi hover (desktop) dan press."""
    _original_elevation = 2

    def on_enter(self):
        anim = Animation(elevation=6, duration=0.15)
        anim.start(self)

    def on_leave(self):
        anim = Animation(elevation=self._original_elevation, duration=0.15)
        anim.start(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Animation(elevation=1, duration=0.08).start(self)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            Animation(elevation=self._original_elevation, duration=0.12).start(self)
        return super().on_touch_up(touch)

class QuickActionButton(MDCard):
    """Tombol aksi cepat berbentuk kotak."""
    icon_name = ""
    button_text = ""
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.md_bg_color = [0.9, 0.9, 0.9, 1]
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.md_bg_color = [1, 1, 1, 1]
        return super().on_touch_up(touch)

# =====================================================================
# KV LANGUAGE - PREMIUM ADMIN DASHBOARD 2026
# =====================================================================
KV = '''
# --- COLOR PALETTE (Navy Professional) ---
# Primary Navy     : 0.11, 0.16, 0.28, 1   (#1C 29 47)
# Accent Navy      : 0.18, 0.27, 0.48, 1   (#2E 45 7A)
# Light Navy Tint  : 0.93, 0.95, 0.98, 1   (#ED F2 FA)

<AdminMenuCard>:
    orientation: "horizontal"
    radius: [18]
    elevation: 2
    md_bg_color: 1, 1, 1, 1
    ripple_behavior: True
    padding: "18dp"
    size_hint_y: None
    height: "82dp"

<QuickActionButton>:
    orientation: "vertical"
    radius: [14]
    elevation: 1
    md_bg_color: 1, 1, 1, 1
    ripple_behavior: True
    padding: "10dp"
    size_hint: None, None
    size: "80dp", "85dp"

<DashboardAdmin>:
    name: 'dashboard_admin'
    md_bg_color: 0.965, 0.973, 0.980, 1

    MDBoxLayout:
        orientation: 'vertical'

        # ===== TOP HEADER BAR (Navy Premium) =====
        MDCard:
            size_hint_y: None
            height: "64dp"
            radius: [0]
            elevation: 3
            md_bg_color: 0.11, 0.16, 0.28, 1
            padding: ["20dp", "0dp", "12dp", "0dp"]
            ripple_behavior: False

            MDBoxLayout:
                orientation: "horizontal"
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "shield-crown-outline"
                    font_size: "26sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.9
                    size_hint_x: None
                    width: "36dp"
                    pos_hint: {"center_y": .5}

                MDBoxLayout:
                    orientation: "vertical"
                    padding: ["10dp", "0dp", "0dp", "0dp"]
                    pos_hint: {"center_y": .5}

                    MDLabel:
                        text: "Administrator Panel"
                        font_style: "H6"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1

                    MDLabel:
                        text: "Manajemen Sistem Penilaian"
                        font_style: "Overline"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.55

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
            bar_color: 0.11, 0.16, 0.28, 0.4

            MDBoxLayout:
                orientation: 'vertical'
                padding: ["20dp", "24dp", "20dp", "30dp"]
                spacing: "20dp"
                adaptive_height: True


                # ===== 1. WELCOME CARD =====
                MDCard:
                    size_hint_y: None
                    height: "120dp"
                    radius: [22]
                    elevation: 4
                    md_bg_color: 0.11, 0.16, 0.28, 1
                    ripple_behavior: False
                    padding: ["24dp", "20dp", "12dp", "20dp"]

                    MDBoxLayout:
                        orientation: "horizontal"

                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "3dp"
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Selamat Datang,"
                                font_style: "Body2"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 0.6
                                size_hint_y: None
                                height: "22dp"
                                shorten: True

                            MDLabel:
                                id: lbl_admin_name
                                text: "Administrator"
                                font_style: "H5"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                size_hint_y: None
                                height: "36dp"
                                shorten: True

                            Widget:
                                size_hint_y: None
                                height: "4dp"

                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint: None, None
                                width: "140dp"
                                height: "26dp"
                                spacing: "6dp"
                                md_bg_color: 1, 1, 1, 0.15
                                radius: [13]
                                padding: ["10dp", "0dp", "14dp", "0dp"]

                                MDIcon:
                                    icon: "shield-crown"
                                    font_size: "14sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.85, 0.65, 0.13, 1
                                    size_hint_x: None
                                    width: "20dp"
                                    pos_hint: {"center_y": .5}

                                MDLabel:
                                    text: "Super Admin"
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 0.85
                                    pos_hint: {"center_y": .5}
                                    shorten: True

                        MDBoxLayout:
                            size_hint_x: None
                            width: "80dp"

                            MDIcon:
                                icon: "cog-outline"
                                font_size: "68sp"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 0.1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                # ===== 2. QUICK ACTIONS =====
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "10dp"

                    MDLabel:
                        text: "Aksi Cepat"
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.14, 0.17, 1

                    ScrollView:
                        do_scroll_y: False
                        size_hint_y: None
                        height: "90dp"
                        bar_width: 0

                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_width: True
                            spacing: "12dp"
                            padding: ["2dp", "2dp", "2dp", "2dp"]

                            QuickActionButton:
                                on_release: root.go_to_kelola_guru()
                                MDIcon:
                                    icon: "account-plus-outline"
                                    font_size: "28sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.25, 0.40, 0.78, 1
                                    halign: "center"
                                MDLabel:
                                    text: "Tambah\\nGuru"
                                    font_style: "Caption"
                                    halign: "center"
                                    theme_text_color: "Secondary"

                            QuickActionButton:
                                on_release: root.go_to_kelola_siswa()
                                MDIcon:
                                    icon: "account-child-outline"
                                    font_size: "28sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.13, 0.55, 0.33, 1
                                    halign: "center"
                                MDLabel:
                                    text: "Tambah\\nSiswa"
                                    font_style: "Caption"
                                    halign: "center"
                                    theme_text_color: "Secondary"

                            QuickActionButton:
                                on_release: root.go_to_kelola_pengumuman()
                                MDIcon:
                                    icon: "bullhorn-outline"
                                    font_size: "28sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.85, 0.65, 0.13, 1
                                    halign: "center"
                                MDLabel:
                                    text: "Buat\\nInfo"
                                    font_style: "Caption"
                                    halign: "center"
                                    theme_text_color: "Secondary"


                # ===== 3. STATISTIK CARDS (Horizontal Scroll) =====
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: "10dp"

                    MDLabel:
                        text: "Ringkasan Sistem"
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.14, 0.17, 1

                    ScrollView:
                        do_scroll_y: False
                        size_hint_y: None
                        height: "115dp"
                        bar_width: 0

                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_width: True
                            spacing: "14dp"
                            padding: ["2dp", "2dp", "2dp", "2dp"]

                            # Card Total Guru
                            MDCard:
                                size_hint: None, None
                                size: "140dp", "110dp"
                                radius: [18]
                                elevation: 2
                                md_bg_color: 1, 1, 1, 1
                                padding: "16dp"
                                orientation: "vertical"

                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "36dp"
                                    MDBoxLayout:
                                        size_hint: None, None
                                        size: "36dp", "36dp"
                                        md_bg_color: 0.88, 0.93, 1.0, 1
                                        radius: [10]
                                        MDIcon:
                                            icon: "account-tie-outline"
                                            font_size: "20sp"
                                            theme_text_color: "Custom"
                                            text_color: 0.25, 0.40, 0.78, 1
                                            halign: "center"
                                            pos_hint: {"center_y": .5}

                                Widget:
                                    size_hint_y: None
                                    height: "8dp"

                                MDLabel:
                                    id: stat_guru
                                    text: "0"
                                    font_style: "H5"
                                    bold: True

                                MDLabel:
                                    text: "Total Guru"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"

                            # Card Total Siswa
                            MDCard:
                                size_hint: None, None
                                size: "140dp", "110dp"
                                radius: [18]
                                elevation: 2
                                md_bg_color: 1, 1, 1, 1
                                padding: "16dp"
                                orientation: "vertical"

                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "36dp"
                                    MDBoxLayout:
                                        size_hint: None, None
                                        size: "36dp", "36dp"
                                        md_bg_color: 0.85, 0.95, 0.90, 1
                                        radius: [10]
                                        MDIcon:
                                            icon: "school-outline"
                                            font_size: "20sp"
                                            theme_text_color: "Custom"
                                            text_color: 0.13, 0.55, 0.33, 1
                                            halign: "center"
                                            pos_hint: {"center_y": .5}

                                Widget:
                                    size_hint_y: None
                                    height: "8dp"

                                MDLabel:
                                    id: stat_siswa
                                    text: "0"
                                    font_style: "H5"
                                    bold: True

                                MDLabel:
                                    text: "Total Siswa"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"

                            # Card Total Penilaian
                            MDCard:
                                size_hint: None, None
                                size: "140dp", "110dp"
                                radius: [18]
                                elevation: 2
                                md_bg_color: 1, 1, 1, 1
                                padding: "16dp"
                                orientation: "vertical"

                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "36dp"
                                    MDBoxLayout:
                                        size_hint: None, None
                                        size: "36dp", "36dp"
                                        md_bg_color: 1.0, 0.9, 0.9, 1
                                        radius: [10]
                                        MDIcon:
                                            icon: "clipboard-check-outline"
                                            font_size: "20sp"
                                            theme_text_color: "Custom"
                                            text_color: 0.8, 0.2, 0.2, 1
                                            halign: "center"
                                            pos_hint: {"center_y": .5}

                                Widget:
                                    size_hint_y: None
                                    height: "8dp"

                                MDLabel:
                                    id: stat_penilaian
                                    text: "0"
                                    font_style: "H5"
                                    bold: True

                                MDLabel:
                                    text: "Data Penilaian"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"

                            # Card Total Laporan
                            MDCard:
                                size_hint: None, None
                                size: "140dp", "110dp"
                                radius: [18]
                                elevation: 2
                                md_bg_color: 1, 1, 1, 1
                                padding: "16dp"
                                orientation: "vertical"

                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "36dp"
                                    MDBoxLayout:
                                        size_hint: None, None
                                        size: "36dp", "36dp"
                                        md_bg_color: 0.9, 0.85, 1.0, 1
                                        radius: [10]
                                        MDIcon:
                                            icon: "file-document-outline"
                                            font_size: "20sp"
                                            theme_text_color: "Custom"
                                            text_color: 0.5, 0.1, 0.8, 1
                                            halign: "center"
                                            pos_hint: {"center_y": .5}

                                Widget:
                                    size_hint_y: None
                                    height: "8dp"

                                MDLabel:
                                    id: stat_laporan
                                    text: "0"
                                    font_style: "H5"
                                    bold: True

                                MDLabel:
                                    text: "Total Laporan"
                                    font_style: "Caption"
                                    theme_text_color: "Secondary"


                # ===== 4. AKTIVITAS TERBARU & MENU =====
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "12dp"
                    adaptive_height: True

                    MDLabel:
                        text: "Pengumuman Aktif"
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.14, 0.17, 1
                    
                    MDList:
                        id: list_aktivitas
                        md_bg_color: 1, 1, 1, 1
                        radius: [12]

                    Widget:
                        size_hint_y: None
                        height: "10dp"

                    MDLabel:
                        text: "Menu Utama"
                        font_style: "Subtitle2"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.14, 0.17, 1

                    # --- Menu 1: Kelola Guru ---
                    AdminMenuCard:
                        on_release: root.go_to_kelola_guru()
                        MDBoxLayout:
                            size_hint: None, None
                            size: "46dp", "46dp"
                            md_bg_color: 0.88, 0.93, 1.0, 1
                            radius: [14]
                            pos_hint: {"center_y": .5}
                            MDIcon:
                                icon: "account-edit-outline"
                                font_size: "22sp"
                                theme_text_color: "Custom"
                                text_color: 0.25, 0.40, 0.78, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: ["16dp", "8dp", "0dp", "8dp"]
                            pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "Manajemen Data Guru"
                                font_style: "Subtitle2"
                                bold: True
                            MDLabel:
                                text: "Tambah, edit, dan hapus akun guru"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                        MDIcon:
                            icon: "chevron-right"
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Hint"

                    # --- Menu 2: Kelola Siswa ---
                    AdminMenuCard:
                        on_release: root.go_to_kelola_siswa()
                        MDBoxLayout:
                            size_hint: None, None
                            size: "46dp", "46dp"
                            md_bg_color: 0.85, 0.95, 0.90, 1
                            radius: [14]
                            pos_hint: {"center_y": .5}
                            MDIcon:
                                icon: "account-school-outline"
                                font_size: "22sp"
                                theme_text_color: "Custom"
                                text_color: 0.13, 0.55, 0.33, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: ["16dp", "8dp", "0dp", "8dp"]
                            pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "Manajemen Data Siswa"
                                font_style: "Subtitle2"
                                bold: True
                            MDLabel:
                                text: "Data induk siswa dan kelas"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                        MDIcon:
                            icon: "chevron-right"
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Hint"

                    # --- Menu 3: Kelola Pengumuman ---
                    AdminMenuCard:
                        on_release: root.go_to_kelola_pengumuman()
                        MDBoxLayout:
                            size_hint: None, None
                            size: "46dp", "46dp"
                            md_bg_color: 1.0, 0.95, 0.85, 1
                            radius: [14]
                            pos_hint: {"center_y": .5}
                            MDIcon:
                                icon: "bullhorn-outline"
                                font_size: "22sp"
                                theme_text_color: "Custom"
                                text_color: 0.85, 0.65, 0.13, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}
                        MDBoxLayout:
                            orientation: "vertical"
                            padding: ["16dp", "8dp", "0dp", "8dp"]
                            pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "Kelola Pengumuman"
                                font_style: "Subtitle2"
                                bold: True
                            MDLabel:
                                text: "Broadcast pesan ke orang tua"
                                font_style: "Caption"
                                theme_text_color: "Secondary"
                        MDIcon:
                            icon: "chevron-right"
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Hint"


                # ===== FOOTER =====
                Widget:
                    size_hint_y: None
                    height: "20dp"

                MDLabel:
                    text: "TK Islam Plus Miftahul Jannah - Admin Panel v2.0"
                    font_style: "Overline"
                    halign: "center"
                    theme_text_color: "Hint"
                    size_hint_y: None
                    height: "20dp"
'''

Builder.load_string(KV)


# =====================================================================
# PYTHON LOGIC
# =====================================================================
class DashboardAdmin(Screen):
    def on_enter(self):
        self.load_stats()
        self.load_aktivitas()
        if current_user.get('nama_lengkap'):
            self.ids.lbl_admin_name.text = current_user['nama_lengkap']

    def load_stats(self):
        """Memuat statistik lengkap."""
        self.ids.stat_guru.text = str(GuruModel.count())
        self.ids.stat_siswa.text = str(SiswaModel.count())
        self.ids.stat_penilaian.text = str(PenilaianModel.count())
        self.ids.stat_laporan.text = str(LaporanModel.count())

    def load_aktivitas(self):
        """Memuat pengumuman terbaru ke list."""
        self.ids.list_aktivitas.clear_widgets()
        pengumuman = PengumumanModel.get_latest(limit=3)
        
        if not pengumuman:
            from kivymd.uix.list import OneLineListItem
            self.ids.list_aktivitas.add_widget(OneLineListItem(text="Tidak ada pengumuman aktif."))
            return
            
        for p in pengumuman:
            item = TwoLineAvatarIconListItem(
                text=p['judul'],
                secondary_text=p['tanggal'].strftime('%d %b %Y') if p.get('tanggal') else "Baru",
                on_release=lambda x: self.go_to_kelola_pengumuman()
            )
            item.add_widget(IconLeftWidget(icon="bell-ring-outline"))
            self.ids.list_aktivitas.add_widget(item)

    def logout(self):
        clear_session()
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'

    def go_to_kelola_guru(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'kelola_guru'

    def go_to_kelola_siswa(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'kelola_siswa'

    def go_to_kelola_pengumuman(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'kelola_pengumuman'

    def go_to_profil(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'profil_admin'