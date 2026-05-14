from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget
from models.penilaian import PenilaianModel

KV = '''
<RiwayatPenilaianScreen>:
    name: 'riwayat_penilaian'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: 'vertical'

        # --- Top App Bar ---
        MDTopAppBar:
            title: "Riwayat Penilaian"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0, 0.5, 0, 1
            elevation: 0

        # --- Search Bar ---
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            padding: "10dp"
            md_bg_color: 1, 1, 1, 1
            elevation: 1
            
            MDTextField:
                id: search_field
                hint_text: "Cari Siswa atau Indikator..."
                mode: "round"
                icon_right: "magnify"
                icon_right_color: 0, 0.5, 0, 1
                on_text: root.filter_data(self.text)

        # --- List Container ---
        ScrollView:
            MDList:
                id: list_riwayat
                padding: "10dp"
'''

Builder.load_string(KV)

class RiwayatPenilaianScreen(Screen):
    def on_enter(self):
        self.ids.search_field.text = ""
        self.load_data()

    def load_data(self, query=""):
        self.ids.list_riwayat.clear_widgets()
        
        # Ambil data dari model
        data = PenilaianModel.get_all_with_filter(search_query=query)
        
        if not data:
            from kivymd.uix.list import OneLineListItem
            self.ids.list_riwayat.add_widget(
                OneLineListItem(text="Tidak ada data penilaian ditemukan.")
            )
            return

        teks_nilai = {
            1: "BB",
            2: "MB",
            3: "BSH",
            4: "BSB"
        }

        for row in data:
            nilai_str = teks_nilai.get(row['nilai'], str(row['nilai']))
            catatan_teks = row['catatan'] if row['catatan'] else "Tidak ada catatan"
            
            # Format tampilan item
            item = ThreeLineAvatarIconListItem(
                text=f"{row['nama_siswa']} ({row['kelas']})",
                secondary_text=f"[{row['tgl']}] Indikator: {row['indikator']}",
                tertiary_text=f"Nilai: {nilai_str} | Catatan: {catatan_teks}"
            )
            
            # Ikon kiri
            icon = IconLeftWidget(icon="clipboard-text-outline")
            icon.theme_text_color = "Custom"
            icon.text_color = [0, 0.5, 0, 1] # Hijau
            item.add_widget(icon)
            
            self.ids.list_riwayat.add_widget(item)

    def filter_data(self, query):
        self.load_data(query)

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_guru'
