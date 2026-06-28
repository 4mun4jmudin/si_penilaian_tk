# pyrefly: ignore [missing-import]
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconRightWidget, IconLeftWidget
from kivymd.toast import toast
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from models.siswa import SiswaModel
from models.user import UserModel

KV = '''
<KelolaSiswaScreen>:
    name: 'kelola_siswa'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Kelola Data Siswa"
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
                hint_text: "Cari Nama Siswa atau Kelas..."
                mode: "round"
                icon_right: "magnify"
                on_text: root.filter_data(self.text)

        ScrollView:
            MDList:
                id: list_siswa
                padding: "10dp"
                spacing: "5dp"

    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: 0.2, 0.6, 0.8, 1 # Biru Terang
        pos_hint: {"right": .95, "bottom": .05}
        on_release: root.open_dialog()

<ContentSiswaDialog>:
    orientation: "vertical"
    spacing: "10dp"
    size_hint_y: None
    height: "340dp"

    MDTextField:
        id: field_nama
        hint_text: "Nama Siswa"
        icon_right: "account"
    
    MDTextField:
        id: field_kelas
        hint_text: "Kelas (Ketuk untuk pilih)"
        icon_right: "chevron-down"
        readonly: True
        on_focus: if self.focus: root.open_kelas_menu()
    
    MDTextField:
        id: field_ortu
        hint_text: "Nama Orang Tua / Wali"
        icon_right: "human-child"
    
    MDTextField:
        id: field_tgl
        hint_text: "Tanggal Lahir"
        icon_right: "calendar"
        readonly: True
        on_focus: if self.focus: root.show_date_picker()

    MDTextField:
        id: field_akun_ortu
        hint_text: "Hubungkan ke Akun Ortu (Ketuk)"
        icon_right: "account-arrow-right"
        readonly: True
        on_focus: if self.focus: root.open_akun_ortu_menu()
'''

Builder.load_string(KV)

class ContentSiswaDialog(MDBoxLayout):
    selected_ortu_id = None  # Menyimpan ID user ortu yang dipilih

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kelas_menu = None
        self.akun_ortu_menu = None

    def open_kelas_menu(self):
        menu_items = [
            {"text": "TK-A", "viewclass": "OneLineListItem", "on_release": lambda x="TK-A": self.set_kelas(x)},
            {"text": "TK-B", "viewclass": "OneLineListItem", "on_release": lambda x="TK-B": self.set_kelas(x)},
        ]
        self.kelas_menu = MDDropdownMenu(
            caller=self.ids.field_kelas,
            items=menu_items,
            width_mult=4,
        )
        self.kelas_menu.open()

    def set_kelas(self, text_item):
        self.ids.field_kelas.text = text_item
        self.kelas_menu.dismiss()

    def open_akun_ortu_menu(self):
        """Menampilkan dropdown daftar akun role OrangTua."""
        ortu_users = UserModel.get_by_role('OrangTua')
        
        menu_items = [
            {
                "text": "-- Tidak Ada (Lepas) --",
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.set_akun_ortu(None, "-- Tidak Ada --"),
            }
        ]
        
        for u in ortu_users:
            menu_items.append({
                "text": u['username'],
                "viewclass": "OneLineListItem",
                "on_release": lambda uid=u['id'], uname=u['username']: self.set_akun_ortu(uid, uname),
            })
        
        self.akun_ortu_menu = MDDropdownMenu(
            caller=self.ids.field_akun_ortu,
            items=menu_items,
            width_mult=5,
        )
        self.akun_ortu_menu.open()

    def set_akun_ortu(self, user_id, username):
        self.selected_ortu_id = user_id
        self.ids.field_akun_ortu.text = username if user_id else "-- Tidak Ada --"
        self.akun_ortu_menu.dismiss()

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    def on_save_date(self, instance, value, date_range):
        self.ids.field_tgl.text = str(value)

class KelolaSiswaScreen(Screen):
    dialog = None
    data_master = []
    editing_id_siswa = None

    def on_enter(self):
        self.load_data()

    def load_data(self):
        self.ids.list_siswa.clear_widgets()
        self.data_master = SiswaModel.get_all()
        self.display_list(self.data_master)

    def display_list(self, data):
        self.ids.list_siswa.clear_widgets()
        
        # Ambil mapping user ortu untuk menampilkan nama akun
        ortu_users = UserModel.get_by_role('OrangTua')
        ortu_map = {u['id']: u['username'] for u in ortu_users}
        
        for siswa in data:
            # Tentukan info akun ortu
            id_ortu = siswa.get('id_user_ortu')
            akun_ortu_text = ortu_map.get(id_ortu, "Belum dihubungkan") if id_ortu else "Belum dihubungkan"
            
            item = ThreeLineAvatarIconListItem(
                text=siswa['nama'],
                secondary_text=f"Kelas: {siswa['kelas']}  |  Ortu: {siswa['nama_orang_tua']}",
                tertiary_text=f"Akun Ortu: {akun_ortu_text}",
                on_release=lambda x, s=siswa: self.open_dialog(s) # Klik untuk Edit
            )
            # Warnai icon hijau jika sudah terhubung, abu-abu jika belum
            icon_color = (0.2, 0.6, 0.3, 1) if id_ortu else (0.6, 0.6, 0.6, 1)
            item.add_widget(IconLeftWidget(
                icon="account-check" if id_ortu else "account-alert-outline",
                theme_text_color="Custom",
                text_color=icon_color,
            ))
            
            btn_hapus = IconRightWidget(
                icon="trash-can-outline",
                theme_text_color="Error",
                on_release=lambda x, sid=siswa['id_siswa']: self.confirm_delete(sid)
            )
            item.add_widget(btn_hapus)
            self.ids.list_siswa.add_widget(item)

    def filter_data(self, query):
        query = query.lower()
        filtered = [s for s in self.data_master if query in s['nama'].lower() or query in s['kelas'].lower()]
        self.display_list(filtered)

    def open_dialog(self, siswa_data=None):
        if not self.dialog:
            self.content_cls = ContentSiswaDialog()
            self.dialog = MDDialog(
                title="Form Data Siswa",
                type="custom",
                content_cls=self.content_cls,
                buttons=[
                    MDFlatButton(text="BATAL", on_release=self.close_dialog),
                    MDFillRoundFlatButton(text="SIMPAN", on_release=self.save_data),
                ],
            )

        # Ambil daftar akun ortu untuk referensi
        ortu_users = UserModel.get_by_role('OrangTua')
        ortu_map = {u['id']: u['username'] for u in ortu_users}

        if siswa_data:
            # MODE EDIT
            self.editing_id_siswa = siswa_data['id_siswa']
            self.content_cls.ids.field_nama.text = siswa_data['nama']
            self.content_cls.ids.field_kelas.text = siswa_data['kelas']
            self.content_cls.ids.field_ortu.text = siswa_data['nama_orang_tua']
            self.content_cls.ids.field_tgl.text = str(siswa_data['tanggal_lahir']) if siswa_data['tanggal_lahir'] else ""
            
            # Set akun ortu yang sudah terhubung
            id_ortu = siswa_data.get('id_user_ortu')
            if id_ortu and id_ortu in ortu_map:
                self.content_cls.selected_ortu_id = id_ortu
                self.content_cls.ids.field_akun_ortu.text = ortu_map[id_ortu]
            else:
                self.content_cls.selected_ortu_id = None
                self.content_cls.ids.field_akun_ortu.text = ""
            
            self.dialog.title = "Edit Data Siswa"
        else:
            # MODE TAMBAH
            self.editing_id_siswa = None
            self.content_cls.ids.field_nama.text = ""
            self.content_cls.ids.field_kelas.text = ""
            self.content_cls.ids.field_ortu.text = ""
            self.content_cls.ids.field_tgl.text = ""
            self.content_cls.ids.field_akun_ortu.text = ""
            self.content_cls.selected_ortu_id = None
            self.dialog.title = "Tambah Siswa Baru"
        
        self.dialog.open()

    def save_data(self, instance):
        nama = self.content_cls.ids.field_nama.text.strip()
        kelas = self.content_cls.ids.field_kelas.text.strip()
        ortu = self.content_cls.ids.field_ortu.text.strip()
        tgl = self.content_cls.ids.field_tgl.text.strip()
        selected_ortu_id = self.content_cls.selected_ortu_id

        if not nama or not kelas:
            toast("Nama dan Kelas wajib diisi!")
            return
            
        if len(nama) < 3:
            toast("Nama minimal 3 karakter!")
            return

        val_tgl = tgl if tgl else None
        
        if self.editing_id_siswa:
            if SiswaModel.update(self.editing_id_siswa, nama, kelas, ortu, val_tgl):
                # Update relasi akun ortu
                SiswaModel.link_ortu(self.editing_id_siswa, selected_ortu_id)
                toast("Data Siswa Diperbarui!")
            else:
                toast("Gagal memperbarui data.")
                return
        else:
            new_id = SiswaModel.create(nama, kelas, ortu, val_tgl, id_user_ortu=selected_ortu_id)
            if new_id:
                toast("Siswa Baru Ditambahkan!")
            else:
                toast("Gagal menyimpan data.")
                return
        
        self.close_dialog()
        self.load_data()

    def confirm_delete(self, id_siswa):
        if not hasattr(self, 'dialog_hapus') or not self.dialog_hapus:
            self.dialog_hapus = MDDialog(
                title="Hapus Siswa?",
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
        self.delete_target = id_siswa
        self.dialog_hapus.open()

    def execute_delete(self):
        if self.delete_target:
            if SiswaModel.delete(self.delete_target):
                toast("Data Siswa dihapus.")
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