from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.toast import toast
from models.pengumuman import PengumumanModel

KV = '''
<KelolaPengumumanScreen>:
    name: 'kelola_pengumuman'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Kelola Pengumuman"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0.1, 0.15, 0.25, 1
            elevation: 0

        # Search Bar
        MDBoxLayout:
            size_hint_y: None
            height: "65dp"
            padding: "10dp"
            md_bg_color: 1, 1, 1, 1
            elevation: 1
            
            MDTextField:
                id: search_field
                hint_text: "Cari Judul Pengumuman..."
                mode: "round"
                icon_right: "magnify"
                on_text: root.filter_data(self.text)

        ScrollView:
            MDList:
                id: list_pengumuman
                padding: "10dp"
                spacing: "5dp"

    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: 0.1, 0.15, 0.25, 1
        pos_hint: {"right": .95, "bottom": .05}
        on_release: root.open_dialog()

<ContentPengumumanDialog>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    height: "200dp"

    MDTextField:
        id: field_judul
        hint_text: "Judul Pengumuman"
        icon_right: "format-title"
    
    MDTextField:
        id: field_isi
        hint_text: "Isi Pengumuman"
        multiline: True
        max_height: "100dp"
'''

Builder.load_string(KV)

class ContentPengumumanDialog(MDBoxLayout):
    pass

class KelolaPengumumanScreen(Screen):
    dialog = None
    data_master = []

    def on_enter(self):
        self.load_data()

    def load_data(self):
        self.ids.list_pengumuman.clear_widgets()
        self.data_master = PengumumanModel.get_all()
        self.display_list(self.data_master)

    def display_list(self, data):
        self.ids.list_pengumuman.clear_widgets()
        for p in data:
            isi_preview = f"{p['isi'][:40]}..." if len(p['isi']) > 40 else p['isi']
            item = TwoLineAvatarIconListItem(
                text=p['judul'],
                secondary_text=f"{p['tanggal']} | {isi_preview}",
                on_release=lambda x, p_data=p: self.open_dialog(p_data)
            )
            item.add_widget(IconLeftWidget(icon="bullhorn-outline"))
            
            btn_hapus = IconRightWidget(
                icon="trash-can-outline",
                theme_text_color="Error",
                on_release=lambda x, pid=p['id_pengumuman']: self.confirm_delete(pid)
            )
            item.add_widget(btn_hapus)
            self.ids.list_pengumuman.add_widget(item)

    def filter_data(self, query):
        query = query.lower()
        filtered = [p for p in self.data_master if query in p['judul'].lower()]
        self.display_list(filtered)

    def open_dialog(self, p_data=None):
        if not self.dialog:
            self.content_cls = ContentPengumumanDialog()
            self.dialog = MDDialog(
                title="Form Pengumuman",
                type="custom",
                content_cls=self.content_cls,
                buttons=[
                    MDFlatButton(text="BATAL", on_release=self.close_dialog),
                    MDFillRoundFlatButton(text="SIMPAN", on_release=self.save_data),
                ],
            )
            
        if p_data:
            self.editing_id = p_data['id_pengumuman']
            self.content_cls.ids.field_judul.text = p_data['judul']
            self.content_cls.ids.field_isi.text = p_data['isi']
            self.dialog.title = "Edit Pengumuman"
        else:
            self.editing_id = None
            self.content_cls.ids.field_judul.text = ""
            self.content_cls.ids.field_isi.text = ""
            self.dialog.title = "Tambah Pengumuman"
            
        self.dialog.open()

    def save_data(self, instance):
        judul = self.content_cls.ids.field_judul.text.strip()
        isi = self.content_cls.ids.field_isi.text.strip()

        if not judul or not isi:
            Snackbar(text="Judul dan isi wajib diisi!", bg_color=(0.8, 0.2, 0.2, 1)).open()
            return

        if self.editing_id:
            if PengumumanModel.update(self.editing_id, judul, isi):
                toast("Pengumuman Diperbarui!")
                self.close_dialog()
                self.load_data()
            else:
                toast("Gagal memperbarui.")
        else:
            if PengumumanModel.create(judul, isi):
                toast("Pengumuman Ditambahkan!")
                self.close_dialog()
                self.load_data()
            else:
                toast("Gagal menyimpan.")

    def confirm_delete(self, id_pengumuman):
        if not hasattr(self, 'dialog_hapus') or not self.dialog_hapus:
            self.dialog_hapus = MDDialog(
                title="Hapus Pengumuman?",
                text="Pengumuman ini akan dihapus permanen.",
                buttons=[
                    MDFlatButton(text="BATAL", on_release=lambda x: self.dialog_hapus.dismiss()),
                    MDFillRoundFlatButton(
                        text="HAPUS", 
                        md_bg_color=(0.8, 0.2, 0.2, 1),
                        on_release=lambda x: self.execute_delete()
                    ),
                ],
            )
        self.delete_target = id_pengumuman
        self.dialog_hapus.open()

    def execute_delete(self):
        if self.delete_target:
            if PengumumanModel.delete(self.delete_target):
                toast("Pengumuman dihapus.")
                self.load_data()
            else:
                toast("Gagal menghapus.")
        if self.dialog_hapus:
            self.dialog_hapus.dismiss()

    def close_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_admin'
