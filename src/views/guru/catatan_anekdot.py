from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from datetime import date
from models.siswa import SiswaModel
from models.anekdot import AnekdotModel
from config.session import current_user

KV = '''
<CatatanAnekdotScreen>:
    name: 'catatan_anekdot'
    md_bg_color: 0.965, 0.973, 0.980, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Catatan Anekdot"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0.13, 0.55, 0.33, 1
            elevation: 0
            specific_text_color: 1, 1, 1, 1

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                adaptive_height: True
                
                MDList:
                    id: list_anekdot
                    spacing: "8dp"

    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: 0.13, 0.55, 0.33, 1
        pos_hint: {"right": .95, "bottom": .05}
        on_release: root.open_dialog()

<ContentAnekdotDialog>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "280dp"

    MDLabel:
        text: "Pilih Siswa"
        font_style: "Caption"
        theme_text_color: "Secondary"

    MDRectangleFlatButton:
        id: btn_pilih_siswa
        text: "Pilih Siswa..."
        pos_hint: {"center_x": .5}
        size_hint_x: 1
        on_release: root.open_siswa_menu()
        text_color: 0.13, 0.55, 0.33, 1
        line_color: 0.13, 0.55, 0.33, 1
        
    MDTextField:
        id: field_tanggal
        hint_text: "Tanggal (YYYY-MM-DD)"
        icon_right: "calendar"
        mode: "rectangle"
        
    MDTextField:
        id: field_catatan
        hint_text: "Tulis catatan perkembangan / anekdot..."
        multiline: True
        mode: "rectangle"
        max_height: "120dp"
'''

Builder.load_string(KV)

class ContentAnekdotDialog(MDBoxLayout):
    screen_ref = None

    def open_siswa_menu(self):
        if self.screen_ref and self.screen_ref.menu_siswa:
            self.screen_ref.menu_siswa.open()

class CatatanAnekdotScreen(Screen):
    dialog = None
    menu_siswa = None
    data_siswa = []
    selected_id_siswa = None

    def on_enter(self):
        self.load_data_siswa()
        self.load_anekdot()

    def load_data_siswa(self):
        self.data_siswa = SiswaModel.get_all()
        menu_items = [
            {
                "text": f"{s['nama']} ({s['kelas']})",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=s: self.set_selected_siswa(x),
            } for s in self.data_siswa
        ]
        self.menu_siswa = MDDropdownMenu(
            caller=None, # will be set in open_dialog
            items=menu_items,
            width_mult=4,
        )

    def set_selected_siswa(self, siswa):
        self.selected_id_siswa = siswa['id_siswa']
        if self.dialog:
            self.dialog.content_cls.ids.btn_pilih_siswa.text = f"Siswa: {siswa['nama']}"
        self.menu_siswa.dismiss()

    def load_anekdot(self):
        self.ids.list_anekdot.clear_widgets()
        data = AnekdotModel.get_all(limit=50)
        
        if not data:
            from kivymd.uix.label import MDLabel
            self.ids.list_anekdot.add_widget(
                MDLabel(text="Belum ada catatan harian.", halign="center", theme_text_color="Hint", padding=[0, 20, 0, 0])
            )
            return

        for d in data:
            item = TwoLineAvatarIconListItem(
                text=d['nama'],
                secondary_text=f"[{d['tanggal']}] {d['catatan']}",
                bg_color=(1,1,1,1)
            )
            item.add_widget(IconLeftWidget(icon="notebook-outline"))
            btn_del = IconRightWidget(icon="delete-outline", theme_text_color="Error")
            btn_del.bind(on_release=lambda x, id=d['id_anekdot']: self.hapus_anekdot(id))
            item.add_widget(btn_del)
            self.ids.list_anekdot.add_widget(item)

    def open_dialog(self):
        content = ContentAnekdotDialog()
        content.screen_ref = self
        content.ids.field_tanggal.text = str(date.today())
        
        self.dialog = MDDialog(
            title="Tambah Catatan Anekdot",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog.dismiss()),
                MDFillRoundFlatButton(
                    text="SIMPAN", 
                    md_bg_color=(0.13, 0.55, 0.33, 1),
                    on_release=lambda x: self.simpan_anekdot()
                ),
            ],
        )
        self.menu_siswa.caller = self.dialog.content_cls.ids.btn_pilih_siswa
        self.dialog.open()

    def simpan_anekdot(self):
        if not self.selected_id_siswa:
            toast("Pilih siswa terlebih dahulu!")
            return
        
        tgl = self.dialog.content_cls.ids.field_tanggal.text
        cttn = self.dialog.content_cls.ids.field_catatan.text
        
        if not cttn:
            toast("Catatan tidak boleh kosong!")
            return
            
        # Simpan ke DB
        id_guru = current_user.get('id_guru') or current_user.get('ID_GURU')
        res = AnekdotModel.create(self.selected_id_siswa, id_guru, tgl, cttn)
        
        if res:
            toast("Catatan berhasil disimpan!")
            self.dialog.dismiss()
            self.load_anekdot()
        else:
            toast("Gagal menyimpan catatan")

    def hapus_anekdot(self, id_anekdot):
        if AnekdotModel.delete(id_anekdot):
            toast("Catatan dihapus")
            self.load_anekdot()

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_guru'
