from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from models.siswa import SiswaModel
from models.penilaian import PenilaianModel
from models.laporan import LaporanModel

KV = '''
<GenerateLaporanScreen>:
    name: 'generate_laporan'
    md_bg_color: 1, 1, 1, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Generate Laporan"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0, 0.5, 0, 1

        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "20dp"
            
            MDLabel:
                text: "Pilih Parameter Laporan"
                font_style: "H6"
                bold: True
                size_hint_y: None
                height: "40dp"

            # Dropdown Pilih Siswa
            MDFillRoundFlatButton:
                id: btn_pilih_siswa
                text: "Pilih Siswa"
                pos_hint: {"center_x": .5}
                size_hint_x: 1
                on_release: root.open_siswa_menu()
                md_bg_color: 0.2, 0.2, 0.2, 1

            MDTextField:
                id: field_periode
                hint_text: "Periode (Contoh: Ganjil 2025)"
                mode: "rectangle"

            Widget:
                size_hint_y: 1 # Spacer pengisi ruang kosong

            MDFillRoundFlatButton:
                text: "GENERATE & LIHAT LAPORAN"
                pos_hint: {"center_x": .5}
                size_hint_x: 1
                md_bg_color: 0, 0.5, 0, 1
                font_size: "18sp"
                on_release: root.do_generate()
'''

Builder.load_string(KV)

class GenerateLaporanScreen(Screen):
    selected_id_siswa = None
    siswa_menu = None
    data_siswa_list = []

    def on_enter(self):
        self.load_siswa_for_menu()

    def load_siswa_for_menu(self):
        self.data_siswa_list = SiswaModel.get_all()

        # Buat item menu dropdown
        menu_items = []
        for s in self.data_siswa_list:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": f"{s['nama']} ({s['kelas']})",
                "on_release": lambda x=s['id_siswa'], t=s['nama']: self.select_siswa(x, t)
            })
        
        self.siswa_menu = MDDropdownMenu(
            caller=self.ids.btn_pilih_siswa,
            items=menu_items,
            width_mult=4,
            max_height="300dp"
        )

    def open_siswa_menu(self):
        if self.siswa_menu:
            self.siswa_menu.open()

    def select_siswa(self, id_siswa, nama):
        self.selected_id_siswa = id_siswa
        self.ids.btn_pilih_siswa.text = nama
        self.ids.btn_pilih_siswa.md_bg_color = [0, 0.5, 0, 1]
        self.siswa_menu.dismiss()

    def apply_rule_based(self, nilai_list):
        """
        Algoritma Sederhana Rule-Based:
        Menghitung rata-rata nilai dan mengonversi ke predikat.
        """
        if not nilai_list:
            return "Belum ada data penilaian."
        
        rata_rata = sum(nilai_list) / len(nilai_list)
        
        # Rule Logic
        if rata_rata >= 3.5:
            return f"Berkembang Sangat Baik (BSB) - Skor: {rata_rata:.2f}"
        elif rata_rata >= 2.5:
            return f"Berkembang Sesuai Harapan (BSH) - Skor: {rata_rata:.2f}"
        elif rata_rata >= 1.5:
            return f"Mulai Berkembang (MB) - Skor: {rata_rata:.2f}"
        else:
            return f"Belum Berkembang (BB) - Skor: {rata_rata:.2f}"

    def do_generate(self):
        periode = self.ids.field_periode.text
        if not self.selected_id_siswa or not periode:
            toast("Pilih Siswa dan Isi Periode!")
            return

        # 1. Ambil data detail nilai mentah via Model
        details = PenilaianModel.get_details_by_siswa(self.selected_id_siswa)
        
        if not details:
            toast("Tidak ada data penilaian untuk siswa ini.")
            return

        # Ekstrak list nilai integer untuk dihitung rata-ratanya
        nilai_list = [d['nilai'] for d in details]

        # 2. Jalankan Rule-Based
        kesimpulan = self.apply_rule_based(nilai_list)
        
        # Build JSON dictionary
        import json
        for d in details:
            if hasattr(d['tgl'], 'isoformat'):
                d['tgl'] = d['tgl'].isoformat()
            # pastikan nilai aman dari null
            if not d.get('catatan'):
                d['catatan'] = "Tidak ada catatan."
                
        hasil_dict = {
            "kesimpulan": kesimpulan,
            "detail": details
        }
        hasil_json = json.dumps(hasil_dict)

        # 3. Simpan ke Tabel Laporan via Model
        last_id = LaporanModel.create(
            id_siswa=self.selected_id_siswa,
            periode=periode,
            hasil=hasil_json
        )
        
        if last_id:
            toast("Laporan Berhasil Dibuat!")
            # Navigasi ke Preview
            preview_screen = self.manager.get_screen('preview_laporan')
            preview_screen.load_report(last_id)
            self.manager.transition.direction = 'left'
            self.manager.current = 'preview_laporan'
        else:
            toast("Gagal membuat laporan.")

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_guru'