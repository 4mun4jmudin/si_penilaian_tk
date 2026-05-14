from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.toast import toast
import re
from models.guru import GuruModel
from models.user import UserModel

KV = '''
<KelolaGuruScreen>:
    name: 'kelola_guru'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Kelola Guru"
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
                hint_text: "Cari Username, NIP atau Nama Guru..."
                mode: "round"
                icon_right: "magnify"
                on_text: root.filter_data(self.text)

        ScrollView:
            MDList:
                id: list_guru
                padding: "10dp"
                spacing: "5dp"

    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: 0.1, 0.15, 0.25, 1
        pos_hint: {"right": .95, "bottom": .05}
        on_release: root.open_dialog() # Mode Tambah

# Dialog Content Layout
<ContentGuruDialog>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    height: "280dp"

    MDTextField:
        id: field_nama
        hint_text: "Nama Lengkap"
        icon_right: "account"
    
    MDTextField:
        id: field_username
        hint_text: "Username Login"
        icon_right: "account-circle"

    MDTextField:
        id: field_nip
        hint_text: "NIP (Opsional, Bisa untuk Login)"
        icon_right: "card-account-details"
    
    MDTextField:
        id: field_password
        hint_text: "Password"
        icon_right: "key"
        password: False
'''

Builder.load_string(KV)

class ContentGuruDialog(MDBoxLayout):
    pass

class KelolaGuruScreen(Screen):
    dialog = None
    data_master = []
    editing_id_guru = None
    editing_id_user = None

    def on_enter(self):
        self.load_data()

    def load_data(self):
        self.ids.list_guru.clear_widgets()
        self.data_master = GuruModel.get_all()
        self.display_list(self.data_master)

    def display_list(self, data):
        self.ids.list_guru.clear_widgets()
        for guru in data:
            nip_str = f" | NIP: {guru['nip']}" if guru['nip'] else ""
            item = TwoLineAvatarIconListItem(
                text=guru['nama'],
                secondary_text=f"User: {guru['username']}{nip_str}",
                on_release=lambda x, g=guru: self.open_dialog(g)
            )
            item.add_widget(IconLeftWidget(icon="account-tie"))
            
            btn_hapus = IconRightWidget(
                icon="trash-can-outline",
                theme_text_color="Error",
                on_release=lambda x, gid=guru['id_guru'], uid=guru['id_user']: self.confirm_delete(gid, uid)
            )
            item.add_widget(btn_hapus)
            self.ids.list_guru.add_widget(item)

    def filter_data(self, query):
        query = query.lower()
        filtered = [
            g for g in self.data_master 
            if query in g['nama'].lower() 
            or query in g['username'].lower() 
            or (g['nip'] and query in str(g['nip']).lower())
        ]
        self.display_list(filtered)

    def open_dialog(self, guru_data=None):
        if not self.dialog:
            self.content_cls = ContentGuruDialog()
            self.dialog = MDDialog(
                title="Form Data Guru",
                type="custom",
                content_cls=self.content_cls,
                buttons=[
                    MDFlatButton(text="BATAL", on_release=self.close_dialog),
                    MDFillRoundFlatButton(text="SIMPAN", on_release=self.save_data),
                ],
            )

        if guru_data:
            self.editing_id_guru = guru_data['id_guru']
            self.editing_id_user = guru_data['id_user']
            self.content_cls.ids.field_nama.text = guru_data['nama']
            self.content_cls.ids.field_username.text = guru_data['username']
            self.content_cls.ids.field_nip.text = guru_data['nip'] or ""
            self.content_cls.ids.field_password.text = ""
            self.content_cls.ids.field_password.hint_text = "Password Baru (Opsional)"
            self.dialog.title = "Edit Data Guru"
        else:
            self.editing_id_guru = None
            self.editing_id_user = None
            self.content_cls.ids.field_nama.text = ""
            self.content_cls.ids.field_username.text = ""
            self.content_cls.ids.field_nip.text = ""
            self.content_cls.ids.field_password.text = "123456"
            self.content_cls.ids.field_password.hint_text = "Password Awal"
            self.dialog.title = "Tambah Guru Baru"
        
        self.dialog.open()

    def save_data(self, instance):
        nama = self.content_cls.ids.field_nama.text.strip()
        username = self.content_cls.ids.field_username.text.strip()
        nip = self.content_cls.ids.field_nip.text.strip() or None
        password = self.content_cls.ids.field_password.text.strip()

        if not nama or not username:
            toast("Nama dan Username wajib diisi!")
            return
            
        try:
            if self.editing_id_guru:
                # Update Guru
                GuruModel.update(self.editing_id_guru, nama, nip)
                # Update User
                if password:
                    UserModel.update_credentials(self.editing_id_user, username, password)
                else:
                    UserModel.update_username(self.editing_id_user, username)
                toast("Data Guru Diperbarui!")
            else:
                # Cek username
                new_user_id = UserModel.create(username, password, role='Guru')
                if new_user_id:
                    GuruModel.create(new_user_id, nama, nip)
                    toast("Guru Baru Ditambahkan!")
                else:
                    toast("Gagal membuat akun (Username mungkin sudah dipakai).")
                    return

            self.close_dialog()
            self.load_data()
            
        except Exception as e:
            toast(f"Error: {e}")

    def confirm_delete(self, id_guru, id_user):
        if not hasattr(self, 'dialog_hapus') or not self.dialog_hapus:
            self.dialog_hapus = MDDialog(
                title="Hapus Guru?",
                text="Tindakan ini tidak bisa dibatalkan.",
                buttons=[
                    MDFlatButton(text="BATAL", on_release=lambda x: self.dialog_hapus.dismiss()),
                    MDFillRoundFlatButton(
                        text="HAPUS", 
                        md_bg_color=(0.8, 0.2, 0.2, 1),
                        on_release=lambda x: self.execute_delete()
                    ),
                ],
            )
        self.delete_target = (id_guru, id_user)
        self.dialog_hapus.open()

    def execute_delete(self):
        if self.delete_target:
            id_guru, id_user = self.delete_target
            if UserModel.delete(id_user):
                toast("Data Guru dihapus.")
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