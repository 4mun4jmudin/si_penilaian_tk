from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from config.session import current_user
from models.user import UserModel
from models.siswa import SiswaModel
import os
import shutil
import threading

KV = '''
<EditProfilOrtuScreen>:
    name: 'edit_profil_ortu'
    md_bg_color: 0.975, 0.970, 0.965, 1

    MDBoxLayout:
        orientation: "vertical"

        # HEADER
        MDBoxLayout:
            size_hint_y: None
            height: "64dp"
            md_bg_color: 0.91, 0.45, 0.14, 1
            padding: ["12dp", "0dp", "12dp", "0dp"]

            MDIconButton:
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": .5}
                on_release: root.kembali()

            MDLabel:
                text: "Edit Profil Orang Tua"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": .5}

        # SCROLL CONTENT
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "20dp"
                adaptive_height: True

                # Card Data Ortu
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    radius: [16]
                    elevation: 2
                    md_bg_color: 1, 1, 1, 1
                    adaptive_height: True

                    MDLabel:
                        text: "Data Orang Tua"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Primary"

                    MDTextField:
                        id: input_nama_ortu
                        hint_text: "Nama Lengkap"

                    MDTextField:
                        id: input_no_hp
                        hint_text: "Nomor Telepon (WA)"

                    MDTextField:
                        id: input_email
                        hint_text: "Email"

                    MDTextField:
                        id: input_alamat
                        hint_text: "Alamat Lengkap"
                        multiline: True

                    # Foto Ortu
                    MDBoxLayout:
                        orientation: "horizontal"
                        adaptive_height: True
                        spacing: "12dp"
                        
                        MDBoxLayout:
                            size_hint: None, None
                            size: dp(80), dp(80)
                            md_bg_color: 0.9, 0.9, 0.9, 1
                            radius: [40]
                            
                            FitImage:
                                id: img_ortu
                                source: ""
                                radius: [40]
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "4dp"
                            pos_hint: {"center_y": .5}
                            
                            MDLabel:
                                text: "Foto Profil Anda"
                                font_style: "Subtitle2"
                                
                            MDRectangleFlatButton:
                                text: "Pilih Foto"
                                text_color: 0.91, 0.45, 0.14, 1
                                on_release: root.pilih_foto('ortu')

                # Card Data Anak
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    radius: [16]
                    elevation: 2
                    md_bg_color: 1, 1, 1, 1
                    adaptive_height: True

                    MDLabel:
                        text: "Data Anak"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Primary"

                    MDLabel:
                        text: "Jenis Kelamin Anak"
                        font_style: "Caption"
                        theme_text_color: "Secondary"

                    MDBoxLayout:
                        adaptive_height: True
                        spacing: "12dp"

                        MDRectangleFlatButton:
                            id: btn_jk_l
                            text: "Laki-laki"
                            text_color: (1,1,1,1) if root.jk_terpilih == 'L' else (0.5,0.5,0.5,1)
                            md_bg_color: (0.91, 0.45, 0.14, 1) if root.jk_terpilih == 'L' else (0,0,0,0)
                            on_release: root.pilih_jk('L')

                        MDRectangleFlatButton:
                            id: btn_jk_p
                            text: "Perempuan"
                            text_color: (1,1,1,1) if root.jk_terpilih == 'P' else (0.5,0.5,0.5,1)
                            md_bg_color: (0.91, 0.45, 0.14, 1) if root.jk_terpilih == 'P' else (0,0,0,0)
                            on_release: root.pilih_jk('P')

                    # Foto Anak
                    MDBoxLayout:
                        orientation: "horizontal"
                        adaptive_height: True
                        spacing: "12dp"
                        
                        MDBoxLayout:
                            size_hint: None, None
                            size: dp(80), dp(80)
                            md_bg_color: 0.9, 0.9, 0.9, 1
                            radius: [40]
                            
                            FitImage:
                                id: img_anak
                                source: ""
                                radius: [40]
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "4dp"
                            pos_hint: {"center_y": .5}
                            
                            MDLabel:
                                text: "Foto Anak"
                                font_style: "Subtitle2"
                                
                            MDRectangleFlatButton:
                                text: "Pilih Foto"
                                text_color: 0.91, 0.45, 0.14, 1
                                on_release: root.pilih_foto('anak')

                Widget:
                    size_hint_y: None
                    height: "10dp"

                MDFillRoundFlatButton:
                    text: "SIMPAN PERUBAHAN"
                    md_bg_color: 0.13, 0.55, 0.33, 1  # Hijau Success
                    size_hint_x: 1
                    on_release: root.simpan_profil()
'''

Builder.load_string(KV)

from kivy.properties import StringProperty

class EditProfilOrtuScreen(Screen):
    jk_terpilih = StringProperty("")
    siswa_data = None
    path_foto_anak = ""
    path_foto_ortu = ""

    def on_enter(self):
        self.load_data()

    def load_data(self):
        user_id = current_user.get('id_user')
        siswa = SiswaModel.get_by_id_user_ortu(user_id)
        self.siswa_data = siswa
        
        if siswa:
            self.ids.input_nama_ortu.text = siswa.get('nama_orang_tua') or ""
            self.ids.input_no_hp.text = siswa.get('no_hp_ortu') or ""
            self.ids.input_email.text = siswa.get('email_ortu') or ""
            self.ids.input_alamat.text = siswa.get('alamat') or ""
            self.jk_terpilih = siswa.get('jenis_kelamin') or ""
            
            # Load foto paths
            self.path_foto_anak = siswa.get('foto_anak') or ""
            self.path_foto_ortu = siswa.get('foto_ortu') or ""
            
            if self.path_foto_anak and os.path.exists(self.path_foto_anak):
                self.ids.img_anak.source = self.path_foto_anak
            else:
                self.ids.img_anak.source = ""
                
            if self.path_foto_ortu and os.path.exists(self.path_foto_ortu):
                self.ids.img_ortu.source = self.path_foto_ortu
            else:
                self.ids.img_ortu.source = ""
        else:
            self.ids.input_nama_ortu.text = ""
            self.ids.input_no_hp.text = ""
            self.ids.input_email.text = ""
            self.ids.input_alamat.text = ""
            self.jk_terpilih = ""

    def pilih_jk(self, jk):
        self.jk_terpilih = jk

    def pilih_foto(self, target):
        """Membuka file dialog untuk memilih foto menggunakan tkinter."""
        def _open_dialog():
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                filepath = filedialog.askopenfilename(
                    title=f"Pilih Foto {target.capitalize()}",
                    filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
                )
                root.destroy()
                if filepath:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.proses_foto(filepath, target), 0)
            except Exception as e:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: toast(f"Error: {e}"), 0)

        threading.Thread(target=_open_dialog, daemon=True).start()

    def proses_foto(self, source_path, target):
        if source_path:
            upload_dir = os.path.join(os.getcwd(), 'assets', 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            filename = os.path.basename(source_path)
            dest_path = os.path.join(upload_dir, f"{target}_{current_user['id_user']}_{filename}")
            
            shutil.copy2(source_path, dest_path)
            
            if target == 'anak':
                self.path_foto_anak = dest_path
                self.ids.img_anak.source = dest_path
            else:
                self.path_foto_ortu = dest_path
                self.ids.img_ortu.source = dest_path
                
            toast(f"Foto {target} berhasil dipilih!")

    def simpan_profil(self):
        if not self.siswa_data:
            toast("Data anak belum dihubungkan ke akun ini.")
            return

        nama_ortu = self.ids.input_nama_ortu.text
        no_hp = self.ids.input_no_hp.text
        email = self.ids.input_email.text
        alamat = self.ids.input_alamat.text
        jk = self.jk_terpilih

        sukses = SiswaModel.update(
            id_siswa=self.siswa_data['id_siswa'],
            nama=self.siswa_data['nama'],
            kelas=self.siswa_data['kelas'],
            nama_orang_tua=nama_ortu,
            tanggal_lahir=self.siswa_data['tanggal_lahir'],
            alamat=alamat,
            jenis_kelamin=jk,
            foto_anak=self.path_foto_anak,
            foto_ortu=self.path_foto_ortu,
            no_hp_ortu=no_hp,
            email_ortu=email
        )

        if sukses:
            toast("Data profil berhasil disimpan!")
            self.kembali()
        else:
            toast("Gagal menyimpan profil.")

    def kembali(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'profil_ortu'
