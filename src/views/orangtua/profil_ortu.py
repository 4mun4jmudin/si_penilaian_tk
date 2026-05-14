from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from config.session import current_user
from models.user import UserModel
from models.siswa import SiswaModel
import os

KV = '''
<ProfilOrtuScreen>:
    name: 'profil_ortu'
    md_bg_color: 0.975, 0.982, 0.992, 1

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Profil Orang Tua"
            left_action_items: [["arrow-left", lambda x: root.kembali()]]
            md_bg_color: 1, 1, 1, 1
            elevation: 0
            specific_text_color: 0.12, 0.16, 0.25, 1
            left_action_color: 0.12, 0.16, 0.25, 1

        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: "16dp"
                spacing: "16dp"
                adaptive_height: True

                # ===== PROFILE CARD =====
                MDCard:
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [22]
                    elevation: 2
                    md_bg_color: 0.97, 0.98, 1, 1
                    padding: "16dp"

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: "14dp"
                        adaptive_height: True

                        # Avatar
                        MDCard:
                            size_hint: None, None
                            size: dp(92), dp(92)
                            radius: [46]
                            elevation: 0
                            md_bg_color: 0.93, 0.95, 1, 1
                            padding: "4dp"
                            pos_hint: {"center_y": .5}

                            FitImage:
                                id: img_ortu
                                source: "assets/default_avatar.png"
                                radius: [42]

                        # Info
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "8dp"
                            adaptive_height: True
                            pos_hint: {"center_y": .5}

                            MDBoxLayout:
                                orientation: "horizontal"
                                adaptive_height: True

                                MDLabel:
                                    id: lbl_nama_ortu
                                    text: "Nama Orang Tua"
                                    font_style: "H6"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0.11, 0.16, 0.28, 1
                                    shorten: True
                                    adaptive_height: True

                                MDFlatButton:
                                    text: "Edit Profil"
                                    theme_text_color: "Custom"
                                    text_color: 0.14, 0.42, 0.82, 1
                                    md_bg_color: 0.93, 0.96, 1, 1
                                    size_hint_x: None
                                    width: dp(104)
                                    on_release: root.go_to_edit()

                            MDLabel:
                                text: "Orang Tua"
                                font_style: "Caption"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                md_bg_color: 0.14, 0.42, 0.82, 1
                                size_hint: None, None
                                size: dp(80), dp(24)
                                halign: "center"
                                valign: "middle"
                                radius: [12]

                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "8dp"
                                adaptive_height: True

                                MDBoxLayout:
                                    orientation: "horizontal"
                                    spacing: "10dp"
                                    adaptive_height: True

                                    MDIcon:
                                        icon: "phone"
                                        theme_text_color: "Custom"
                                        text_color: 0.43, 0.48, 0.58, 1
                                        font_size: "18sp"
                                        size_hint: None, None
                                        size: dp(20), dp(20)

                                    MDLabel:
                                        id: lbl_no_hp
                                        text: "-"
                                        font_style: "Body2"
                                        theme_text_color: "Custom"
                                        text_color: 0.18, 0.22, 0.30, 1
                                        shorten: True
                                        adaptive_height: True

                                MDBoxLayout:
                                    orientation: "horizontal"
                                    spacing: "10dp"
                                    adaptive_height: True

                                    MDIcon:
                                        icon: "email-outline"
                                        theme_text_color: "Custom"
                                        text_color: 0.43, 0.48, 0.58, 1
                                        font_size: "18sp"
                                        size_hint: None, None
                                        size: dp(20), dp(20)

                                    MDLabel:
                                        id: lbl_email
                                        text: "-"
                                        font_style: "Body2"
                                        theme_text_color: "Custom"
                                        text_color: 0.18, 0.22, 0.30, 1
                                        shorten: True
                                        adaptive_height: True

                                MDBoxLayout:
                                    orientation: "horizontal"
                                    spacing: "10dp"
                                    adaptive_height: True

                                    MDIcon:
                                        icon: "home-outline"
                                        theme_text_color: "Custom"
                                        text_color: 0.43, 0.48, 0.58, 1
                                        font_size: "18sp"
                                        size_hint: None, None
                                        size: dp(20), dp(20)

                                    MDLabel:
                                        id: lbl_alamat
                                        text: "-"
                                        font_style: "Body2"
                                        theme_text_color: "Custom"
                                        text_color: 0.18, 0.22, 0.30, 1
                                        shorten: True
                                        adaptive_height: True

                # ===== DATA ANAK =====
                MDCard:
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [22]
                    elevation: 2
                    md_bg_color: 1, 1, 1, 1
                    padding: "16dp"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "12dp"
                        adaptive_height: True

                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_height: True
                            spacing: "8dp"

                            MDIcon:
                                icon: "account-child-outline"
                                theme_text_color: "Custom"
                                text_color: 0.14, 0.42, 0.82, 1
                                font_size: "20sp"
                                size_hint: None, None
                                size: dp(22), dp(22)

                            MDLabel:
                                text: "Data Anak"
                                font_style: "Subtitle1"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.11, 0.16, 0.28, 1
                                adaptive_height: True

                        MDLabel:
                            text: "Data anak yang terhubung dengan akun ini"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0.45, 0.50, 0.60, 1
                            adaptive_height: True

                        MDCard:
                            size_hint_y: None
                            height: self.minimum_height
                            radius: [18]
                            elevation: 0
                            md_bg_color: 0.98, 0.99, 1, 1
                            padding: "12dp"

                            MDBoxLayout:
                                orientation: "horizontal"
                                spacing: "12dp"
                                adaptive_height: True

                                MDCard:
                                    size_hint: None, None
                                    size: dp(60), dp(60)
                                    radius: [30]
                                    elevation: 0
                                    md_bg_color: 0.92, 0.95, 1, 1
                                    padding: "2dp"
                                    pos_hint: {"center_y": .5}

                                    FitImage:
                                        id: img_anak
                                        source: "assets/default_avatar.png"
                                        radius: [28]

                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: "4dp"
                                    adaptive_height: True
                                    pos_hint: {"center_y": .5}

                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        adaptive_height: True

                                        MDLabel:
                                            id: lbl_nama_anak
                                            text: "Belum Dihubungkan"
                                            font_style: "Subtitle2"
                                            bold: True
                                            theme_text_color: "Custom"
                                            text_color: 0.12, 0.16, 0.25, 1
                                            shorten: True
                                            adaptive_height: True

                                        MDLabel:
                                            text: "Aktif"
                                            font_style: "Caption"
                                            bold: True
                                            halign: "center"
                                            valign: "middle"
                                            theme_text_color: "Custom"
                                            text_color: 0.10, 0.58, 0.28, 1
                                            md_bg_color: 0.84, 0.96, 0.88, 1
                                            size_hint: None, None
                                            size: dp(46), dp(22)
                                            radius: [11]

                                    MDLabel:
                                        id: lbl_nisn
                                        text: "Kelas: -"
                                        font_style: "Caption"
                                        theme_text_color: "Custom"
                                        text_color: 0.45, 0.50, 0.60, 1
                                        adaptive_height: True

                                    MDBoxLayout:
                                        orientation: "horizontal"
                                        spacing: "14dp"
                                        adaptive_height: True

                                        MDBoxLayout:
                                            orientation: "horizontal"
                                            spacing: "6dp"
                                            size_hint_x: None
                                            width: dp(110)
                                            adaptive_height: True

                                            MDIcon:
                                                icon: "account-group-outline"
                                                font_size: "16sp"
                                                theme_text_color: "Custom"
                                                text_color: 0.14, 0.42, 0.82, 1
                                                size_hint: None, None
                                                size: dp(18), dp(18)

                                            MDLabel:
                                                id: lbl_kelas_anak
                                                text: "-"
                                                font_style: "Caption"
                                                theme_text_color: "Custom"
                                                text_color: 0.18, 0.22, 0.30, 1
                                                shorten: True
                                                adaptive_height: True

                                        MDBoxLayout:
                                            orientation: "horizontal"
                                            spacing: "6dp"
                                            adaptive_height: True

                                            MDIcon:
                                                icon: "calendar-month-outline"
                                                font_size: "16sp"
                                                theme_text_color: "Custom"
                                                text_color: 0.14, 0.42, 0.82, 1
                                                size_hint: None, None
                                                size: dp(18), dp(18)

                                            MDLabel:
                                                id: lbl_tgl_lahir
                                                text: "-"
                                                font_style: "Caption"
                                                theme_text_color: "Custom"
                                                text_color: 0.18, 0.22, 0.30, 1
                                                shorten: True
                                                adaptive_height: True

                # ===== PENGATURAN AKUN =====
                MDCard:
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [22]
                    elevation: 2
                    md_bg_color: 1, 1, 1, 1
                    padding: "16dp"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "8dp"
                        adaptive_height: True

                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_height: True
                            spacing: "8dp"

                            MDIcon:
                                icon: "lock-outline"
                                theme_text_color: "Custom"
                                text_color: 0.14, 0.42, 0.82, 1
                                font_size: "20sp"
                                size_hint: None, None
                                size: dp(22), dp(22)

                            MDLabel:
                                text: "Pengaturan Akun"
                                font_style: "Subtitle1"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.11, 0.16, 0.28, 1
                                adaptive_height: True

                        MDList:
                            TwoLineAvatarIconListItem:
                                text: "Ubah Password"
                                secondary_text: "Ganti password akun Anda"
                                on_release: root.show_ubah_password()
                                IconLeftWidget:
                                    icon: "key-outline"
                                IconRightWidget:
                                    icon: "chevron-right"

                            TwoLineAvatarIconListItem:
                                text: "Keluar"
                                secondary_text: "Keluar dari akun ini"
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: "logout-variant"
                                    theme_text_color: "Custom"
                                    text_color: 0.92, 0.30, 0.38, 1
                                IconRightWidget:
                                    icon: "chevron-right"

                # ===== INFO AKUN =====
                MDCard:
                    size_hint_y: None
                    height: self.minimum_height
                    radius: [22]
                    elevation: 1
                    md_bg_color: 1, 1, 1, 1
                    padding: "16dp"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: "10dp"
                        adaptive_height: True

                        MDBoxLayout:
                            orientation: "horizontal"
                            adaptive_height: True
                            spacing: "8dp"

                            MDIcon:
                                icon: "information-outline"
                                theme_text_color: "Custom"
                                text_color: 0.14, 0.42, 0.82, 1
                                font_size: "20sp"
                                size_hint: None, None
                                size: dp(22), dp(22)

                            MDLabel:
                                text: "Informasi Akun"
                                font_style: "Subtitle1"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.11, 0.16, 0.28, 1
                                adaptive_height: True

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: "10dp"
                            adaptive_height: True

                            MDCard:
                                size_hint: 0.5, None
                                height: self.minimum_height
                                radius: [16]
                                elevation: 0
                                md_bg_color: 0.98, 0.99, 1, 1
                                padding: "12dp"

                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: "2dp"
                                    adaptive_height: True

                                    MDLabel:
                                        text: "Username"
                                        font_style: "Caption"
                                        theme_text_color: "Custom"
                                        text_color: 0.45, 0.50, 0.60, 1
                                        adaptive_height: True

                                    MDLabel:
                                        id: lbl_username
                                        text: "-"
                                        font_style: "Body2"
                                        bold: True
                                        theme_text_color: "Custom"
                                        text_color: 0.18, 0.22, 0.30, 1
                                        shorten: True
                                        adaptive_height: True

                            MDCard:
                                size_hint: 0.5, None
                                height: self.minimum_height
                                radius: [16]
                                elevation: 0
                                md_bg_color: 0.98, 0.99, 1, 1
                                padding: "12dp"

                                MDBoxLayout:
                                    orientation: "vertical"
                                    spacing: "2dp"
                                    adaptive_height: True

                                    MDLabel:
                                        text: "Peran"
                                        font_style: "Caption"
                                        theme_text_color: "Custom"
                                        text_color: 0.45, 0.50, 0.60, 1
                                        adaptive_height: True

                                    MDLabel:
                                        id: lbl_role
                                        text: "Orang Tua"
                                        font_style: "Body2"
                                        bold: True
                                        theme_text_color: "Custom"
                                        text_color: 0.18, 0.22, 0.30, 1
                                        adaptive_height: True

                Widget:
                    size_hint_y: None
                    height: dp(8)
'''

Builder.load_string(KV)


class ProfilOrtuScreen(Screen):
    def on_enter(self):
        self.load_data()

    def load_data(self):
        user_id = current_user.get('id_user')
        siswa = SiswaModel.get_by_id_user_ortu(user_id)

        self.ids.lbl_username.text = current_user.get('username') or "-"
        self.ids.lbl_role.text = current_user.get('role') or "Orang Tua"

        if siswa:
            self.ids.lbl_nama_ortu.text = siswa.get('nama_orang_tua') or current_user.get('username') or "-"
            self.ids.lbl_no_hp.text = siswa.get('no_hp_ortu') or "-"
            self.ids.lbl_email.text = siswa.get('email_ortu') or "-"
            self.ids.lbl_alamat.text = siswa.get('alamat') or "-"

            path_foto_ortu = siswa.get('foto_ortu')
            if path_foto_ortu and os.path.exists(path_foto_ortu):
                self.ids.img_ortu.source = path_foto_ortu
            else:
                self.ids.img_ortu.source = "assets/default_avatar.png"

            self.ids.lbl_nama_anak.text = siswa.get('nama') or "-"
            self.ids.lbl_nisn.text = f"Kelas: {siswa.get('kelas', '-')}"
            self.ids.lbl_kelas_anak.text = siswa.get('kelas') or "-"

            if siswa.get('tanggal_lahir'):
                self.ids.lbl_tgl_lahir.text = str(siswa['tanggal_lahir'])
            else:
                self.ids.lbl_tgl_lahir.text = "-"

            path_foto_anak = siswa.get('foto_anak')
            if path_foto_anak and os.path.exists(path_foto_anak):
                self.ids.img_anak.source = path_foto_anak
            else:
                self.ids.img_anak.source = "assets/default_avatar.png"
        else:
            self.ids.lbl_nama_ortu.text = current_user.get('username') or "-"
            self.ids.lbl_no_hp.text = "-"
            self.ids.lbl_email.text = "-"
            self.ids.lbl_alamat.text = "-"
            self.ids.lbl_nama_anak.text = "Belum Dihubungkan"
            self.ids.lbl_nisn.text = "Kelas: -"
            self.ids.lbl_kelas_anak.text = "-"
            self.ids.lbl_tgl_lahir.text = "-"
            self.ids.img_ortu.source = "assets/default_avatar.png"
            self.ids.img_anak.source = "assets/default_avatar.png"

    def go_to_edit(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'edit_profil_ortu'

    def show_ubah_password(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.boxlayout import MDBoxLayout

        self.input_pwd = MDTextField(
            hint_text="Password Baru",
            password=True,
            mode="fill",
            size_hint_y=None,
            height=dp(56),
        )

        box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(90),
            padding=(0, dp(4), 0, 0),
        )
        box.add_widget(self.input_pwd)

        self.dialog_pwd = MDDialog(
            title="Ubah Password",
            type="custom",
            content_cls=box,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self.dialog_pwd.dismiss()),
                MDFlatButton(text="SIMPAN", on_release=lambda x: self.simpan_password())
            ]
        )
        self.dialog_pwd.open()

    def simpan_password(self):
        pwd = self.input_pwd.text.strip()
        if not pwd:
            toast("Password tidak boleh kosong")
            return

        sukses = UserModel.update_credentials(
            current_user['id_user'],
            current_user['username'],
            pwd
        )
        if sukses:
            toast("Password berhasil diubah!")
        else:
            toast("Gagal merubah password")

        self.dialog_pwd.dismiss()

    def kembali(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_ortu'

    def logout(self):
        from config.session import clear_session
        clear_session()
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'