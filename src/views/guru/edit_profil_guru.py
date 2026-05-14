from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from config.session import current_user
from models.guru import GuruModel
from models.user import UserModel
import os
import shutil
import threading

KV = '''
<EditProfilGuruScreen>:
    name: 'edit_profil_guru'
    md_bg_color: 0.98, 0.98, 0.98, 1

    MDBoxLayout:
        orientation: "vertical"

        # HEADER
        MDBoxLayout:
            size_hint_y: None
            height: "64dp"
            md_bg_color: 0.13, 0.55, 0.33, 1
            padding: ["12dp", "0dp", "12dp", "0dp"]

            MDIconButton:
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": .5}
                on_release: root.kembali()

            MDLabel:
                text: "Edit Profil Guru"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": .5}

        # SCROLL CONTENT
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp"
                spacing: "24dp"
                adaptive_height: True

                # Card Data Guru
                MDCard:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    radius: [16]
                    elevation: 2
                    md_bg_color: 1, 1, 1, 1
                    adaptive_height: True

                    MDLabel:
                        text: "Data Guru"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Primary"

                    MDTextField:
                        id: input_nama_lengkap
                        hint_text: "Nama Lengkap"
                        mode: "rectangle"

                    MDTextField:
                        id: input_nip
                        hint_text: "NIP / No Identitas"
                        mode: "rectangle"

                    MDTextField:
                        id: input_no_hp
                        hint_text: "No Handphone (WA)"
                        mode: "rectangle"

                    # Foto Guru
                    MDBoxLayout:
                        orientation: "horizontal"
                        adaptive_height: True
                        spacing: "12dp"
                        padding: ["0dp", "8dp", "0dp", "0dp"]
                        
                        MDBoxLayout:
                            size_hint: None, None
                            size: dp(80), dp(80)
                            md_bg_color: 0.9, 0.9, 0.9, 1
                            radius: [40]
                            
                            FitImage:
                                id: img_guru
                                source: "assets/default_avatar.png"
                                radius: [40]
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "4dp"
                            pos_hint: {"center_y": .5}
                            
                            MDLabel:
                                text: "Foto Profil"
                                font_style: "Subtitle2"
                                
                            MDRectangleFlatButton:
                                text: "Pilih Foto"
                                text_color: 0.13, 0.55, 0.33, 1
                                line_color: 0.13, 0.55, 0.33, 1
                                on_release: root.pilih_foto()

                Widget:
                    size_hint_y: None
                    height: "10dp"

                MDFillRoundFlatButton:
                    text: "SIMPAN PERUBAHAN"
                    md_bg_color: 0.13, 0.55, 0.33, 1
                    size_hint_x: 1
                    on_release: root.simpan_profil()
'''

Builder.load_string(KV)

class EditProfilGuruScreen(Screen):
    guru_data = None
    path_foto = ""

    def on_enter(self):
        self.load_data()

    def load_data(self):
        user_id = current_user.get('id_user')
        self.guru_data = GuruModel.get_by_user_id(user_id)
        
        if self.guru_data:
            self.ids.input_nama_lengkap.text = self.guru_data.get('nama') or ""
            self.ids.input_nip.text = self.guru_data.get('nip') or ""
            self.ids.input_no_hp.text = self.guru_data.get('no_hp') or ""
            
            self.path_foto = self.guru_data.get('foto') or ""
            if self.path_foto and os.path.exists(self.path_foto):
                self.ids.img_guru.source = self.path_foto
            else:
                self.ids.img_guru.source = "assets/default_avatar.png"
        else:
            self.ids.input_nama_lengkap.text = ""
            self.ids.input_nip.text = ""
            self.ids.input_no_hp.text = ""
            self.ids.img_guru.source = "assets/default_avatar.png"

    def pilih_foto(self):
        """Membuka file dialog untuk memilih foto menggunakan tkinter."""
        def _open_dialog():
            try:
                import tkinter as tk
                from tkinter import filedialog
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                filepath = filedialog.askopenfilename(
                    title="Pilih Foto Profil Guru",
                    filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
                )
                root.destroy()
                if filepath:
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt: self.proses_foto(filepath), 0)
            except Exception as e:
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: toast(f"Error: {e}"), 0)

        threading.Thread(target=_open_dialog, daemon=True).start()

    def proses_foto(self, source_path):
        if source_path:
            upload_dir = os.path.join(os.getcwd(), 'assets', 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            filename = os.path.basename(source_path)
            dest_path = os.path.join(upload_dir, f"guru_{current_user['id_user']}_{filename}")
            
            try:
                shutil.copy2(source_path, dest_path)
                self.path_foto = dest_path
                self.ids.img_guru.source = dest_path
                toast("Foto berhasil dipilih!")
            except Exception as e:
                toast(f"Gagal menyalin foto: {e}")

    def simpan_profil(self):
        if not self.guru_data:
            toast("Data guru tidak ditemukan.")
            return

        nama = self.ids.input_nama_lengkap.text
        nip = self.ids.input_nip.text
        no_hp = self.ids.input_no_hp.text
        
        id_guru = self.guru_data.get('id_guru') or self.guru_data.get('ID_GURU')
        
        if GuruModel.update(id_guru, nama, nip, no_hp, self.path_foto):
            toast("Profil berhasil diperbarui!")
            # Update session if needed
            from config.session import _current_user
            _current_user['nama_lengkap'] = nama
            self.kembali()
        else:
            toast("Gagal memperbarui profil.")

    def kembali(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'profil_guru'
