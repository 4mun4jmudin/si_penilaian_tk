from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget
from models.siswa import SiswaModel

KV = '''
<DataSiswaScreen>:
    name: 'data_siswa'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: 'vertical'

        # --- HEADER ---
        MDTopAppBar:
            title: "Data Siswa"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0, 0.5, 0, 1
            elevation: 0

        # --- SEARCH BAR ---
        MDCard:
            size_hint_y: None
            height: "60dp"
            md_bg_color: 1, 1, 1, 1
            radius: [0, 0, 10, 10]
            elevation: 1
            padding: "10dp"
            
            MDIcon:
                icon: "magnify"
                pos_hint: {"center_y": .5}
                theme_text_color: "Hint"
            
            TextInput:
                id: search_field
                hint_text: "Cari nama siswa atau kelas..."
                background_color: 0, 0, 0, 0
                foreground_color: 0, 0, 0, 1
                cursor_color: 0, 0.5, 0, 1
                pos_hint: {"center_y": .5}
                padding_y: [15, 0]
                on_text: root.filter_data(self.text)

        # --- LIST SISWA ---
        ScrollView:
            MDList:
                id: container_siswa
                padding: "10dp"
                spacing: "5dp"
'''

Builder.load_string(KV)

class DataSiswaScreen(Screen):
    data_master = [] # Simpan data asli dari DB

    def on_enter(self):
        self.load_data()

    def load_data(self):
        self.ids.container_siswa.clear_widgets()
        self.data_master = SiswaModel.get_all()
        self.display_list(self.data_master)

    def display_list(self, data_list):
        self.ids.container_siswa.clear_widgets()
        
        for siswa in data_list:
            # Format Teks
            nama = siswa['nama']
            info_kelas = f"Kelas: {siswa['kelas']} | Lahir: {siswa['tanggal_lahir']}"
            info_ortu = f"Orang Tua: {siswa['nama_orang_tua']}"

            # Buat Item List (3 Baris)
            item = ThreeLineAvatarIconListItem(
                text=nama,
                secondary_text=info_kelas,
                tertiary_text=info_ortu,
                bg_color=[1, 1, 1, 1],
                theme_text_color="Custom",
                text_color=[0, 0, 0, 0.8]
            )
            
            # Ikon Avatar (Huruf depan nama)
            icon = IconLeftWidget(icon="account")
            item.add_widget(icon)
            
            self.ids.container_siswa.add_widget(item)

    def filter_data(self, query):
        query = query.lower()
        filtered_list = []
        
        for s in self.data_master:
            # Cari berdasarkan Nama atau Kelas
            if query in s['nama'].lower() or query in s['kelas'].lower():
                filtered_list.append(s)
        
        self.display_list(filtered_list)

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_guru'