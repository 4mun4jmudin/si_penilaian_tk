from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu
from datetime import date
from models.penilaian import PenilaianModel
from config.session import current_user

KV = '''
<InputNilaiScreen>:
    name: 'input_nilai'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: 'vertical'

        # --- Top App Bar ---
        MDTopAppBar:
            title: "Input Penilaian"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0, 0.5, 0, 1
            elevation: 0

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "20dp"
                adaptive_height: True

                # --- Card Info Siswa ---
                MDCard:
                    padding: "15dp"
                    radius: [10]
                    md_bg_color: 0.9, 0.98, 0.9, 1 # Hijau muda lembut
                    elevation: 0
                    orientation: "vertical"
                    size_hint_y: None
                    height: "85dp"

                    MDLabel:
                        text: "Menilai Siswa:"
                        font_style: "Caption"
                        theme_text_color: "Secondary"
                    
                    MDLabel:
                        id: label_nama_siswa
                        text: "-"
                        font_style: "H6"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0, 0.5, 0, 1
                
                # --- Form Input ---
                
                # 1. Tanggal
                MDTextField:
                    id: field_tanggal
                    hint_text: "Tanggal (YYYY-MM-DD)"
                    text: root.get_today_date()
                    mode: "rectangle"
                    icon_right: "calendar"
                    icon_right_color: 0, 0.5, 0, 1
                    line_color_focus: 0, 0.5, 0, 1
                
                # 2. Indikator
                MDTextField:
                    id: field_indikator
                    hint_text: "Indikator Penilaian"
                    helper_text: "Contoh: Motorik Halus, Membaca Doa, dll."
                    helper_text_mode: "on_focus"
                    mode: "rectangle"
                    line_color_focus: 0, 0.5, 0, 1
                
                # 3. Pilihan Nilai (Dropdown)
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: "80dp"
                    spacing: "5dp"

                    MDLabel:
                        text: "Hasil Perkembangan:"
                        font_style: "Subtitle2"
                        theme_text_color: "Primary"
                    
                    MDFillRoundFlatButton:
                        id: btn_nilai
                        text: "Pilih Nilai (BB / MB / BSH / BSB)"
                        pos_hint: {"center_x": .5}
                        size_hint_x: 1
                        height: "50dp"
                        md_bg_color: 0.5, 0.5, 0.5, 1 # Abu-abu default
                        on_release: root.open_menu()

                # 4. Catatan Guru & Auto Generate
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    spacing: "5dp"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        
                        MDLabel:
                            text: "Catatan Guru:"
                            font_style: "Subtitle2"
                            theme_text_color: "Primary"
                            size_hint_y: None
                            height: "30dp"
                            
                        MDTextButton:
                            text: "Auto Generate"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1
                            pos_hint: {"center_y": .5}
                            on_release: root.generate_deskripsi()

                    MDTextField:
                        id: field_catatan
                        hint_text: "Ketik catatan atau klik Auto Generate..."
                        mode: "rectangle"
                        multiline: True
                        max_height: "100dp"
                        line_color_focus: 0, 0.5, 0, 1

                # Spacer
                Widget:
                    size_hint_y: None
                    height: "30dp"

                # Tombol Simpan
                MDFillRoundFlatButton:
                    text: "SIMPAN PENILAIAN"
                    md_bg_color: 0, 0.5, 0, 1 # Hijau Utama
                    size_hint_x: 1
                    height: "50dp"
                    font_size: "18sp"
                    on_release: root.save_data()
'''

Builder.load_string(KV)

class InputNilaiScreen(Screen):
    selected_id_siswa = None
    selected_nilai_code = None # Menyimpan angka (1, 2, 3, 4) untuk DB
    menu = None

    def on_enter(self):
        # Inisialisasi Menu Dropdown saat layar dibuka
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "BB (Belum Berkembang)",
                "on_release": lambda x=1, t="BB (Belum Berkembang)": self.set_nilai(x, t),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "MB (Mulai Berkembang)",
                "on_release": lambda x=2, t="MB (Mulai Berkembang)": self.set_nilai(x, t),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "BSH (Berkembang Sesuai Harapan)",
                "on_release": lambda x=3, t="BSH (Berkembang Sesuai Harapan)": self.set_nilai(x, t),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "BSB (Berkembang Sangat Baik)",
                "on_release": lambda x=4, t="BSB (Berkembang Sangat Baik)": self.set_nilai(x, t),
            },
        ]
        
        self.menu = MDDropdownMenu(
            caller=self.ids.btn_nilai,
            items=menu_items,
            width_mult=4,
            max_height="240dp",
        )

    def set_siswa(self, id_siswa, nama):
        """Dipanggil dari halaman PilihSiswaScreen"""
        self.selected_id_siswa = id_siswa
        self.ids.label_nama_siswa.text = nama
        
        # Reset form agar bersih saat ganti siswa
        self.ids.field_indikator.text = ""
        self.ids.field_catatan.text = ""
        self.selected_nilai_code = None
        self.ids.btn_nilai.text = "Pilih Nilai (BB / MB / BSH / BSB)"
        self.ids.btn_nilai.md_bg_color = [0.5, 0.5, 0.5, 1] # Reset ke abu-abu

    def get_today_date(self):
        return str(date.today())

    def open_menu(self):
        if self.menu:
            self.menu.open()

    def set_nilai(self, code, text_label):
        self.selected_nilai_code = code
        self.ids.btn_nilai.text = text_label
        self.ids.btn_nilai.md_bg_color = [0, 0.5, 0, 1] # Ubah jadi hijau
        self.menu.dismiss()

    def generate_deskripsi(self):
        indikator = self.ids.field_indikator.text.strip()
        
        if not indikator or not self.selected_nilai_code:
            toast("Isi indikator dan pilih nilai terlebih dahulu!")
            return
            
        teks_nilai = {
            1: "belum berkembang",
            2: "mulai berkembang",
            3: "berkembang sesuai harapan",
            4: "berkembang sangat baik"
        }
        
        nilai_str = teks_nilai.get(self.selected_nilai_code, "")
        
        # Format kalimat: "Ananda berkembang sesuai harapan dalam indikator [nama indikator]."
        deskripsi = f"Ananda {nilai_str} dalam indikator {indikator.lower()}."
        self.ids.field_catatan.text = deskripsi

    def save_data(self):
        tgl = self.ids.field_tanggal.text
        indikator = self.ids.field_indikator.text
        catatan = self.ids.field_catatan.text
        
        # Ambil ID Guru yang sedang login dari session
        id_guru = current_user.get('id_guru')

        # Validasi Input
        if not self.selected_id_siswa:
            toast("Error: Data siswa tidak ditemukan.")
            return
        if not id_guru:
            toast("Error: Sesi guru berakhir. Silakan login ulang.")
            return
        if not indikator or not self.selected_nilai_code or not tgl:
            toast("Harap lengkapi Indikator dan Nilai!")
            return

        # Simpan ke Database via Model
        result = PenilaianModel.create(
            id_siswa=self.selected_id_siswa,
            id_guru=id_guru,
            tgl=tgl,
            indikator=indikator,
            nilai=self.selected_nilai_code,
            catatan=catatan
        )
        
        if result:
            toast("Data Penilaian Berhasil Disimpan!")
            self.back()
        else:
            toast("Gagal menyimpan data.")

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'pilih_siswa'