from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivymd.uix.card import MDCard
from kivymd.toast import toast
from config.session import current_user, clear_session
from models.siswa import SiswaModel
from models.laporan import LaporanModel
from models.pengumuman import PengumumanModel
import os


# =====================================================================
# KV LANGUAGE - PREMIUM ORANG TUA DASHBOARD 2026
# =====================================================================
KV = '''
# --- COLOR PALETTE (Warm Orange Elegan) ---
# Primary Orange   : 0.91, 0.45, 0.14, 1   (#E8 73 24)
# Dark Orange      : 0.78, 0.35, 0.08, 1
# Light Orange Tint: 1.0, 0.97, 0.94, 1     (#FF F8 F0)
# Surface White    : 1, 1, 1, 1
# Background       : 0.975, 0.970, 0.965, 1 (#F9 F8 F7)

<BubblePengumuman>:
    orientation: "vertical"
    padding: "16dp"
    spacing: "8dp"
    size_hint_y: None
    height: self.minimum_height
    md_bg_color: 1.0, 0.95, 0.85, 1  # Warna orange soft
    radius: [20, 20, 20, 4]  # Bentuk mengelembung
    elevation: 1

    MDBoxLayout:
        orientation: "horizontal"
        adaptive_height: True
        spacing: "10dp"
        
        MDIcon:
            icon: "bell-ring"
            theme_text_color: "Custom"
            text_color: 0.91, 0.45, 0.14, 1
            font_size: "20sp"
            pos_hint: {"center_y": .5}
            
        MDLabel:
            text: root.judul
            font_style: "Subtitle2"
            bold: True
            theme_text_color: "Primary"
            shorten: True
            pos_hint: {"center_y": .5}

    MDLabel:
        text: root.isi
        font_style: "Caption"
        theme_text_color: "Secondary"
        adaptive_height: True

<DashboardOrtu>:
    name: 'dashboard_ortu'
    md_bg_color: 0.975, 0.970, 0.965, 1

    MDBoxLayout:
        orientation: 'vertical'

        # ===== TOP HEADER BAR (Warm Orange) =====
        MDCard:
            size_hint_y: None
            height: "64dp"
            radius: [0]
            elevation: 3
            md_bg_color: 0.91, 0.45, 0.14, 1
            padding: ["20dp", "0dp", "12dp", "0dp"]
            ripple_behavior: False

            MDBoxLayout:
                orientation: "horizontal"
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "home-heart"
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
                        text: "Portal Orang Tua"
                        font_style: "H6"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1

                    MDLabel:
                        text: "TK Miftahul Jannah"
                        font_style: "Overline"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.6

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
            bar_color: 0.91, 0.45, 0.14, 0.4

            MDBoxLayout:
                orientation: 'vertical'
                padding: ["20dp", "24dp", "20dp", "30dp"]
                spacing: "20dp"
                adaptive_height: True


                # ===== 1. PROFIL ANAK CARD =====
                MDCard:
                    size_hint_y: None
                    height: "130dp"
                    radius: [22]
                    elevation: 4
                    md_bg_color: 0.91, 0.45, 0.14, 1
                    ripple_behavior: False
                    padding: ["24dp", "20dp", "12dp", "20dp"]

                    MDBoxLayout:
                        orientation: "horizontal"

                        # Kiri: Text
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "3dp"
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Ananda Tercinta,"
                                font_style: "Body2"
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 0.7
                                size_hint_y: None
                                height: "22dp"
                                shorten: True
                                text_size: self.width, None

                            MDLabel:
                                id: lbl_nama_anak
                                text: "Memuat..."
                                font_style: "H5"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                size_hint_y: None
                                height: "36dp"
                                shorten: True
                                text_size: self.width, None

                            Widget:
                                size_hint_y: None
                                height: "4dp"

                            # Badge Kelas
                            MDBoxLayout:
                                orientation: "horizontal"
                                size_hint: None, None
                                width: "140dp"
                                height: "26dp"
                                spacing: "6dp"
                                md_bg_color: 1, 1, 1, 0.18
                                radius: [13]
                                padding: ["10dp", "0dp", "14dp", "0dp"]

                                MDIcon:
                                    icon: "school"
                                    font_size: "14sp"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 0.9
                                    size_hint_x: None
                                    width: "20dp"
                                    pos_hint: {"center_y": .5}

                                MDLabel:
                                    id: lbl_kelas_anak
                                    text: "Kelas -"
                                    font_style: "Caption"
                                    theme_text_color: "Custom"
                                    text_color: 1, 1, 1, 0.9
                                    pos_hint: {"center_y": .5}
                                    shorten: True
                                    text_size: self.width, None

                        # Kanan: Foto Anak
                        MDCard:
                            size_hint: None, None
                            size: dp(86), dp(86)
                            radius: [43]
                            elevation: 0
                            md_bg_color: 1, 1, 1, 0.2
                            pos_hint: {"center_y": .5}
                            padding: "2dp"
                            
                            FitImage:
                                id: img_foto_anak
                                source: "assets/default_avatar.png"
                                radius: [41]


                # ===== 1.5 QUICK MENU =====
                MDGridLayout:
                    cols: 2
                    spacing: "14dp"
                    adaptive_height: True
                    
                    # Menu Perkembangan Anak
                    MDCard:
                        radius: [18]
                        elevation: 2
                        md_bg_color: 1, 1, 1, 1
                        padding: "16dp"
                        orientation: "vertical"
                        ripple_behavior: True
                        size_hint_y: None
                        height: "110dp"
                        on_release: root.go_to_perkembangan()

                        MDBoxLayout:
                            size_hint: None, None
                            size: "36dp", "36dp"
                            md_bg_color: 0.88, 0.95, 0.90, 1
                            radius: [10]

                            MDIcon:
                                icon: "chart-line-variant"
                                font_size: "20sp"
                                theme_text_color: "Custom"
                                text_color: 0.2, 0.6, 0.3, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                        Widget:
                            size_hint_y: None
                            height: "8dp"

                        MDLabel:
                            text: "Perkembangan"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1

                        MDLabel:
                            text: "Nilai & Catatan"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1

                    # Menu Profil & Data
                    MDCard:
                        radius: [18]
                        elevation: 2
                        md_bg_color: 1, 1, 1, 1
                        padding: "16dp"
                        orientation: "vertical"
                        ripple_behavior: True
                        size_hint_y: None
                        height: "110dp"
                        on_release: root.go_to_profil()

                        MDBoxLayout:
                            size_hint: None, None
                            size: "36dp", "36dp"
                            md_bg_color: 0.95, 0.88, 1.0, 1
                            radius: [10]

                            MDIcon:
                                icon: "account-edit-outline"
                                font_size: "20sp"
                                theme_text_color: "Custom"
                                text_color: 0.5, 0.2, 0.7, 1
                                halign: "center"
                                pos_hint: {"center_y": .5}

                        Widget:
                            size_hint_y: None
                            height: "8dp"

                        MDLabel:
                            text: "Profil Ortu"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1

                        MDLabel:
                            text: "Lengkapi data anak"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1


                # ===== 2. STATISTIK CARDS =====
                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "110dp"
                    spacing: "14dp"

                    # Card Total Laporan
                    MDCard:
                        radius: [18]
                        elevation: 2
                        md_bg_color: 1, 1, 1, 1
                        padding: "16dp"
                        orientation: "vertical"
                        ripple_behavior: True

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: "36dp"

                            MDBoxLayout:
                                size_hint: None, None
                                size: "36dp", "36dp"
                                md_bg_color: 1.0, 0.93, 0.88, 1
                                radius: [10]
                                pos_hint: {"center_y": .5}

                                MDIcon:
                                    icon: "file-document-outline"
                                    font_size: "20sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.91, 0.45, 0.14, 1
                                    halign: "center"
                                    pos_hint: {"center_y": .5}

                            Widget:

                        Widget:
                            size_hint_y: None
                            height: "4dp"

                        MDLabel:
                            id: stat_laporan
                            text: "0"
                            font_style: "H4"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1

                        MDLabel:
                            text: "Total Laporan"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1

                    # Card Semester Aktif
                    MDCard:
                        radius: [18]
                        elevation: 2
                        md_bg_color: 1, 1, 1, 1
                        padding: "16dp"
                        orientation: "vertical"
                        ripple_behavior: True

                        MDBoxLayout:
                            orientation: "horizontal"
                            size_hint_y: None
                            height: "36dp"

                            MDBoxLayout:
                                size_hint: None, None
                                size: "36dp", "36dp"
                                md_bg_color: 0.88, 0.93, 1.0, 1
                                radius: [10]
                                pos_hint: {"center_y": .5}

                                MDIcon:
                                    icon: "calendar-month-outline"
                                    font_size: "20sp"
                                    theme_text_color: "Custom"
                                    text_color: 0.25, 0.47, 0.85, 1
                                    halign: "center"
                                    pos_hint: {"center_y": .5}

                            Widget:

                        Widget:
                            size_hint_y: None
                            height: "4dp"

                        MDLabel:
                            id: stat_semester
                            text: "-"
                            font_style: "H6"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.12, 0.14, 0.17, 1
                            shorten: True
                            shorten_from: 'right'

                        MDLabel:
                            text: "Semester Aktif"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.56, 1


                # ===== 3. PENGUMUMAN TERKINI =====
                MDBoxLayout:
                    size_hint_y: None
                    height: "28dp"
                    padding: ["2dp", "0dp", "0dp", "0dp"]

                    MDLabel:
                        text: "Pengumuman Terkini"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.12, 0.14, 0.17, 1

                MDCard:
                    radius: [18]
                    md_bg_color: 1, 1, 1, 1
                    elevation: 2
                    padding: "16dp"
                    orientation: "vertical"
                    adaptive_height: True

                    MDBoxLayout:
                        id: list_pengumuman_ortu
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: "12dp"


                # ===== 4. TOMBOL RIWAYAT LAPORAN =====
                MDCard:
                    size_hint_y: None
                    height: "64dp"
                    radius: [18]
                    elevation: 3
                    md_bg_color: 0.91, 0.45, 0.14, 1
                    ripple_behavior: True
                    on_release: root.go_to_history()
                    padding: ["20dp", "0dp", "20dp", "0dp"]

                    MDBoxLayout:
                        orientation: "horizontal"
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "file-search-outline"
                            font_size: "24sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            size_hint_x: None
                            width: "32dp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "Lihat Riwayat Laporan Belajar"
                            font_style: "Subtitle2"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 1
                            padding: ["12dp", "0dp", "0dp", "0dp"]
                            pos_hint: {"center_y": .5}
                            shorten: True
                            text_size: self.width, None

                        MDIcon:
                            icon: "chevron-right"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 0.7
                            size_hint_x: None
                            width: "24dp"
                            pos_hint: {"center_y": .5}


                # ===== FOOTER =====
                Widget:
                    size_hint_y: None
                    height: "20dp"

                MDLabel:
                    text: "TK Islam Plus Miftahul Jannah - Portal Orang Tua v2.0"
                    font_style: "Overline"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: 0.45, 0.50, 0.56, 0.5
                    size_hint_y: None
                    height: "20dp"
'''

Builder.load_string(KV)


# =====================================================================
# PYTHON LOGIC
# =====================================================================
from kivy.properties import StringProperty

class BubblePengumuman(MDCard):
    judul = StringProperty("")
    isi = StringProperty("")
    
    def on_enter(self):
        pass

    def on_kv_post(self, base_widget):
        # Efek animasi "mengelembung" / breathing
        anim = Animation(elevation=3, duration=1.2) + Animation(elevation=1, duration=1.2)
        anim.repeat = True
        anim.start(self)

class DashboardOrtu(Screen):
    id_siswa_connected = None

    def on_enter(self):
        self.load_child_data()
        self.load_pengumuman()

    def load_child_data(self):
        user_id = current_user.get('id_user')
        siswa = SiswaModel.get_by_id_user_ortu(user_id)
        
        if siswa:
            self.id_siswa_connected = siswa['id_siswa']
            self.ids.lbl_nama_anak.text = siswa['nama']
            self.ids.lbl_kelas_anak.text = f"Kelas {siswa['kelas']}"
            
            # Load foto anak
            foto = siswa.get('foto_anak')
            if foto and os.path.exists(foto):
                self.ids.img_foto_anak.source = foto
            else:
                self.ids.img_foto_anak.source = "assets/default_avatar.png"

            # Statistik via Model
            total_laporan = LaporanModel.count_by_siswa(siswa['id_siswa'])
            self.ids.stat_laporan.text = str(total_laporan)

            periode = LaporanModel.get_latest_periode_by_siswa(siswa['id_siswa'])
            self.ids.stat_semester.text = periode if periode else "Ganjil 2025"
        else:
            self.ids.lbl_nama_anak.text = "Data Belum Dihubungkan"
            self.ids.lbl_kelas_anak.text = "Harap lapor Admin"

    def load_pengumuman(self):
        self.ids.list_pengumuman_ortu.clear_widgets()
        
        pengumuman_list = PengumumanModel.get_latest(limit=5)

        if not pengumuman_list:
            from kivymd.uix.label import MDLabel
            self.ids.list_pengumuman_ortu.add_widget(
                MDLabel(
                    text="Belum ada pengumuman minggu ini",
                    halign="center",
                    theme_text_color="Hint",
                    font_style="Caption"
                )
            )
        else:
            for p in pengumuman_list:
                item = BubblePengumuman(
                    judul=p['judul'],
                    isi=p['isi']
                )
                self.ids.list_pengumuman_ortu.add_widget(item)

    def go_to_history(self):
        if self.id_siswa_connected:
            history_screen = self.manager.get_screen('history_laporan')
            history_screen.set_siswa(self.id_siswa_connected)

            self.manager.transition.direction = 'left'
            self.manager.current = 'history_laporan'
        else:
            toast("Data anak belum terhubung dengan akun Anda.")

    def go_to_perkembangan(self):
        if self.id_siswa_connected:
            perkembangan_screen = self.manager.get_screen('perkembangan_anak_ortu')
            perkembangan_screen.set_siswa(self.id_siswa_connected)
            self.manager.transition.direction = 'left'
            self.manager.current = 'perkembangan_anak_ortu'
        else:
            toast("Data anak belum terhubung dengan akun Anda.")

    def go_to_profil(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'profil_ortu'

    def logout(self):
        clear_session()
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'