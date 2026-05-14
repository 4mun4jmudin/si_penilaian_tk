from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from models.laporan import LaporanModel

KV = '''
<HistoryLaporanScreen>:
    name: 'history_laporan'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Riwayat Laporan"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 1, 0.4, 0, 1
            elevation: 0

        # List Container
        ScrollView:
            MDList:
                id: list_history
                padding: "10dp"
                spacing: "5dp"
'''

Builder.load_string(KV)

class HistoryLaporanScreen(Screen):
    current_id_siswa = None

    def set_siswa(self, id_siswa):
        self.current_id_siswa = id_siswa
        self.load_history()

    def load_history(self):
        self.ids.list_history.clear_widgets()
        laporan_list = LaporanModel.get_by_siswa(self.current_id_siswa)

        for lap in laporan_list:
            tgl = str(lap['created_at'])
            
            item = TwoLineAvatarIconListItem(
                text=f"Laporan Periode {lap['periode']}",
                secondary_text=f"Dibuat pada: {tgl}",
                on_release=lambda x, lid=lap['id_laporan']: self.go_to_detail(lid)
            )
            
            # Ikon Dokumen
            item.add_widget(IconLeftWidget(
                icon="file-document",
                theme_text_color="Custom",
                text_color=[1, 0.4, 0, 1]
            ))
            
            # Ikon Panah Kanan
            item.add_widget(IconRightWidget(icon="chevron-right"))
            
            self.ids.list_history.add_widget(item)

    def go_to_detail(self, id_laporan):
        detail_screen = self.manager.get_screen('detail_laporan_ortu')
        detail_screen.load_report(id_laporan)
        
        self.manager.transition.direction = 'left'
        self.manager.current = 'detail_laporan_ortu'

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_ortu'