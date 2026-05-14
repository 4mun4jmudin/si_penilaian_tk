from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from models.siswa import SiswaModel

KV = '''
<PilihSiswaScreen>:
    name: 'pilih_siswa'
    md_bg_color: 0.96, 0.96, 0.96, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Pilih Siswa"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0, 0.5, 0, 1
            elevation: 0

        # Search Bar Sederhana
        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: "10dp"
            md_bg_color: 1, 1, 1, 1
            
            MDIcon:
                icon: "magnify"
                pos_hint: {"center_y": .5}
                theme_text_color: "Hint"
            
            TextInput:
                id: search_field
                hint_text: "Cari nama siswa..."
                background_color: 0, 0, 0, 0
                foreground_color: 0, 0, 0, 1
                cursor_color: 0, 0.5, 0, 1
                pos_hint: {"center_y": .5}
                on_text: root.filter_siswa(self.text)

        # List Siswa
        ScrollView:
            MDList:
                id: container_siswa
'''

Builder.load_string(KV)

class PilihSiswaScreen(Screen):
    data_siswa = [] # Menyimpan data mentah dari DB

    def on_enter(self):
        self.load_siswa()

    def load_siswa(self):
        self.ids.container_siswa.clear_widgets()
        self.data_siswa = SiswaModel.get_all()
        self.display_list(self.data_siswa)

    def display_list(self, data):
        self.ids.container_siswa.clear_widgets()
        for siswa in data:
            # Membuat Item List
            item = OneLineAvatarIconListItem(
                text=f"{siswa['nama']} ({siswa['kelas']})",
                on_release=lambda x, s_id=siswa['id_siswa'], s_nama=siswa['nama']: self.go_to_input(s_id, s_nama)
            )
            # Menambahkan Ikon User
            icon = IconLeftWidget(icon="account")
            item.add_widget(icon)
            self.ids.container_siswa.add_widget(item)

    def filter_siswa(self, query):
        # Filter data berdasarkan input search
        filtered_data = [
            s for s in self.data_siswa 
            if query.lower() in s['nama'].lower()
        ]
        self.display_list(filtered_data)

    def go_to_input(self, id_siswa, nama_siswa):
        # Kirim data ke layar input nilai
        input_screen = self.manager.get_screen('input_nilai')
        input_screen.set_siswa(id_siswa, nama_siswa)
        
        self.manager.transition.direction = 'left'
        self.manager.current = 'input_nilai'

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_guru'