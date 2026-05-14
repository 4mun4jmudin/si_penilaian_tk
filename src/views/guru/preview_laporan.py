import os
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

# Import Model Layer & Session
from models.laporan import LaporanModel
from config.session import current_user

# Import PDF Generator yang baru dibuat
from utils.pdf_generator import create_laporan_pdf

# --- KV TETAP SAMA (Hanya Python Logic yang bertambah) ---
KV_PREVIEW = '''
<PreviewLaporanScreen>:
    name: 'preview_laporan'
    md_bg_color: 0.96, 0.96, 0.96, 1

    MDBoxLayout:
        orientation: 'vertical'

        # --- Top App Bar ---
        MDTopAppBar:
            title: "Preview Laporan"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 0, 0.5, 0, 1
            elevation: 2

        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                orientation: 'vertical'
                padding: "16dp"
                spacing: "24dp"
                adaptive_height: True

                # --- DOCUMENT CARD ---
                MDCard:
                    orientation: "vertical"
                    padding: "0dp"
                    radius: [12]
                    md_bg_color: 1, 1, 1, 1
                    elevation: 3
                    adaptive_height: True
                    
                    # 1. Header Kopsurat
                    MDBoxLayout:
                        size_hint_y: None
                        height: "100dp"
                        padding: "20dp"
                        md_bg_color: 0.9, 0.98, 0.9, 1
                        radius: [12, 12, 0, 0]
                        spacing: "15dp"

                        MDIcon:
                            icon: "school"
                            font_size: "48sp"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1
                            pos_hint: {"center_y": .5}
                        
                        MDBoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}
                            adaptive_height: True
                            
                            MDLabel:
                                text: "TK Islam Plus Miftahul Jannah"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0, 0.5, 0, 1
                            
                            MDLabel:
                                text: "Laporan Hasil Belajar Siswa"
                                font_style: "Caption"
                                theme_text_color: "Secondary"

                    # 2. Student Details Section
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "24dp"
                        spacing: "16dp"
                        adaptive_height: True

                        # Nama & Kelas
                        MDGridLayout:
                            cols: 2
                            spacing: "10dp"
                            adaptive_height: True
                            
                            MDBoxLayout:
                                orientation: "vertical"
                                adaptive_height: True
                                MDLabel:
                                    text: "Nama Siswa"
                                    font_style: "Caption"
                                    theme_text_color: "Hint"
                                MDLabel:
                                    text: root.student_name
                                    font_style: "Subtitle1"
                                    bold: True
                                    shorten: True
                            
                            MDBoxLayout:
                                orientation: "vertical"
                                adaptive_height: True
                                size_hint_x: 0.4
                                MDLabel:
                                    text: "Kelas"
                                    font_style: "Caption"
                                    theme_text_color: "Hint"
                                MDLabel:
                                    text: root.student_class
                                    font_style: "Subtitle1"
                                    bold: True

                        # Periode
                        MDBoxLayout:
                            orientation: "vertical"
                            adaptive_height: True
                            MDLabel:
                                text: "Periode Akademik"
                                font_style: "Caption"
                                theme_text_color: "Hint"
                            MDLabel:
                                text: root.report_period
                                font_style: "Subtitle1"
                                bold: True

                        MDSeparator:
                            height: "1dp"

                        # 3. Result Section
                        MDBoxLayout:
                            orientation: "vertical"
                            spacing: "12dp"
                            padding: [0, "10dp", 0, "10dp"]
                            adaptive_height: True

                            MDLabel:
                                text: "Hasil Evaluasi Akhir"
                                font_style: "Subtitle2"
                                theme_text_color: "Primary"
                                halign: "center"
                            
                            MDCard:
                                radius: [8]
                                md_bg_color: 0.95, 0.95, 0.95, 1
                                padding: "20dp"
                                elevation: 0
                                adaptive_height: True
                                
                                MDLabel:
                                    text: root.report_result
                                    font_style: "H6"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.4, 0, 1
                                    halign: "center"
                                    adaptive_height: True 

                            MDLabel:
                                text: "*Penilaian berdasarkan algoritma Rule-Based."
                                font_style: "Overline"
                                theme_text_color: "Hint"
                                halign: "center"
                                italic: True

                    # 4. Footer
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: ["24dp", "0dp", "24dp", "30dp"]
                        adaptive_height: True
                        
                        MDLabel:
                            text: "Mengetahui,"
                            font_style: "Caption"
                            halign: "right"
                        
                        Widget:
                            size_hint_y: None
                            height: "40dp"
                        
                        MDLabel:
                            text: "( Guru Wali Kelas )"
                            font_style: "Body2"
                            bold: True
                            halign: "right"

                # --- ACTION BUTTON ---
                MDFillRoundFlatButton:
                    text: "UNDUH / CETAK PDF"
                    font_size: "16sp"
                    size_hint_x: 1
                    height: "56dp"
                    md_bg_color: 0.8, 0, 0, 1
                    on_release: root.export_pdf()
'''

Builder.load_string(KV_PREVIEW)

class PreviewLaporanScreen(Screen):
    student_name = StringProperty("-")
    student_class = StringProperty("-")
    report_period = StringProperty("-")
    report_result = StringProperty("Memuat data...")
    dialog = None

    def load_report(self, id_laporan):
        data = LaporanModel.get_by_id(id_laporan)
        
        if data:
            self.student_name = data['nama_siswa']
            self.student_class = data['kelas']
            self.report_period = data['periode']
            
            # Parse JSON
            import json
            try:
                hasil_dict = json.loads(data['hasil'])
                self.report_result = hasil_dict.get('kesimpulan', '-')
                self.full_report_data = hasil_dict # Simpan buat PDF
            except json.JSONDecodeError:
                self.report_result = data['hasil']
                self.full_report_data = None
        else:
            toast("Data laporan tidak ditemukan!")

    def export_pdf(self):
        """Membuat file PDF dan menyimpannya."""
        try:
            # 1. Siapkan data untuk PDF Generator
            nama_guru = current_user.get('nama_lengkap', 'Guru Wali Kelas')
            
            pdf_data = {
                'nama': self.student_name,
                'kelas': self.student_class,
                'periode': self.report_period,
                'hasil': getattr(self, 'full_report_data', self.report_result),
                'guru': nama_guru
            }

            # 2. Tentukan Lokasi Penyimpanan
            # Nama file unik: Laporan_NamaSiswa_Periode.pdf
            safe_name = self.student_name.replace(" ", "_")
            filename = f"Laporan_{safe_name}_{self.report_period}.pdf"
            
            filepath = ""

            if platform == 'android':
                # Simpan di folder Downloads pada Android
                try:
                    from android.storage import primary_external_storage_path # type: ignore
                    storage_path = primary_external_storage_path()
                    download_path = os.path.join(storage_path, 'Download')
                except ImportError:
                    print("Modul android.storage tidak ditemukan.")
                    toast("Gagal akses penyimpanan Android.")
                    return
                
                # Buat folder jika belum ada (opsional)
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                    
                filepath = os.path.join(download_path, filename)
            else:
                # Simpan di folder Downloads pada PC (Windows/Mac/Linux)
                home = os.path.expanduser("~")
                download_path = os.path.join(home, 'Downloads')
                
                # Pastikan folder downloads ada (kadang beda di linux server dll)
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                    
                filepath = os.path.join(download_path, filename)

            # 3. Panggil Utility PDF Generator
            create_laporan_pdf(filepath, pdf_data)
            
            # 4. Tampilkan Konfirmasi Sukses
            self.show_success_dialog(filepath)

        except Exception as e:
            print(f"PDF Error: {e}")
            toast(f"Gagal membuat PDF: {e}")

    def show_success_dialog(self, filepath):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Berhasil!",
                text=f"Laporan berhasil disimpan di:\n{filepath}",
                buttons=[
                    MDFlatButton(
                        text="TUTUP",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.text = f"Laporan berhasil disimpan di:\n{filepath}"
        self.dialog.open()

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_guru'