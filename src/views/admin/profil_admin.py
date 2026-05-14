from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from config.session import current_user, clear_session
from models.user import UserModel
import os

KV = '''
<ProfilAdminScreen>:
    name: 'profil_admin'
    md_bg_color: 0.95, 0.96, 0.98, 1

    MDBoxLayout:
        orientation: "vertical"

        # ===== TOP APP BAR =====
        MDTopAppBar:
            title: "Profil Admin"
            left_action_items: [["arrow-left", lambda x: root.kembali()]]
            md_bg_color: 0.95, 0.96, 0.98, 1
            elevation: 0
            specific_text_color: 0.12, 0.16, 0.25, 1
            left_action_color: 0.12, 0.16, 0.25, 1

        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: ["20dp", "10dp", "20dp", "40dp"]
                spacing: "24dp"
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
                                id: img_avatar
                                source: "assets/default_avatar.png"
                                radius: [42]

                        # Info
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "8dp"
                            adaptive_height: True
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                id: lbl_nama
                                text: "Administrator"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.11, 0.16, 0.28, 1
                                shorten: True
                                adaptive_height: True

                            MDLabel:
                                text: "System Admin"
                                font_style: "Caption"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1, 1, 1, 1
                                md_bg_color: 0.11, 0.16, 0.28, 1
                                size_hint: None, None
                                size: dp(94), dp(24)
                                halign: "center"
                                valign: "middle"
                                radius: [12]

                            MDBoxLayout:
                                orientation: "horizontal"
                                spacing: "10dp"
                                adaptive_height: True

                                MDIcon:
                                    icon: "account-badge-outline"
                                    theme_text_color: "Custom"
                                    text_color: 0.43, 0.48, 0.58, 1
                                    font_size: "18sp"
                                    size_hint: None, None
                                    size: dp(20), dp(20)

                                MDLabel:
                                    id: lbl_username
                                    text: "-"
                                    font_style: "Body2"
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
                                text_color: 0.11, 0.16, 0.28, 1
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
                                text: "Keamanan Akun"
                                secondary_text: "Ubah username & password"
                                on_release: root.show_ubah_password()
                                IconLeftWidget:
                                    icon: "shield-check-outline"
                                    theme_text_color: "Custom"
                                    text_color: 0.43, 0.48, 0.58, 1
                                IconRightWidget:
                                    icon: "chevron-right"

                            TwoLineAvatarIconListItem:
                                text: "Keluar"
                                secondary_text: "Keluar dari akun ini"
                                on_release: root.logout()
                                IconLeftWidget:
                                    icon: "logout-variant"
                                    theme_text_color: "Custom"
                                    text_color: 0.8, 0.2, 0.2, 1
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
                                text_color: 0.11, 0.16, 0.28, 1
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
                                        text: "Akun Terdaftar"
                                        font_style: "Caption"
                                        theme_text_color: "Custom"
                                        text_color: 0.45, 0.50, 0.60, 1
                                        adaptive_height: True

                                    MDLabel:
                                        text: "Sistem Utama"
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
                                        text: "Admin"
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

class ProfilAdminScreen(Screen):
    def on_enter(self):
        self.load_data()

    def load_data(self):
        self.ids.lbl_username.text = f"User: {current_user.get('username', '')}"
        self.ids.lbl_nama.text = current_user.get('nama_lengkap') or "Administrator"

    def show_ubah_password(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        from kivymd.uix.textfield import MDTextField
        from kivy.uix.boxlayout import BoxLayout
        
        box = BoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="120dp")
        self.input_pwd = MDTextField(hint_text="Password Baru", password=True)
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
        pwd = self.input_pwd.text
        if pwd:
            sukses = UserModel.update_credentials(current_user['id_user'], current_user['username'], pwd)
            if sukses:
                toast("Password berhasil diubah!")
            else:
                toast("Gagal merubah password")
        self.dialog_pwd.dismiss()

    def kembali(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_admin'

    def logout(self):
        clear_session()
        self.manager.transition.direction = 'down'
        self.manager.current = 'login'
