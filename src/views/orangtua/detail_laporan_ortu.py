import os
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from models.laporan import LaporanModel
from utils.pdf_generator import create_laporan_pdf

KV = '''
<DetailLaporanOrtuScreen>:
    name: 'detail_laporan_ortu'
    md_bg_color: 0.96, 0.96, 0.96, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Detail Laporan"
            left_action_items: [["arrow-left", lambda x: root.back()]]
            md_bg_color: 1, 0.4, 0, 1
            elevation: 2

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "20dp"
                adaptive_height: True

                # --- HEADER ---
                MDBoxLayout:
                    orientation: 'vertical'
                    adaptive_height: True
                    size_hint_y: None
                    spacing: "5dp"
                    
                    MDLabel:
                        text: "Laporan Hasil Belajar"
                        font_style: "H5"
                        bold: True
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 0.4, 0, 1
                        adaptive_height: True
                        size_hint_y: None
                    
                    MDLabel:
                        text: root.student_name
                        font_style: "Subtitle1"
                        halign: "center"
                        theme_text_color: "Secondary"
                        adaptive_height: True
                        size_hint_y: None

                # --- KONTEN LAPORAN ---
                MDCard:
                    orientation: "vertical"
                    padding: "20dp"
                    radius: [12]
                    md_bg_color: 1, 1, 1, 1
                    elevation: 2
                    adaptive_height: True
                    size_hint_y: None
                    spacing: "15dp"

                    # Baris Periode
                    MDBoxLayout:
                        adaptive_height: True
                        size_hint_y: None
                        orientation: "horizontal"
                        spacing: "10dp"
                        
                        MDLabel:
                            text: "Periode:"
                            font_style: "Body2"
                            theme_text_color: "Hint"
                            size_hint_x: 0.3
                            adaptive_height: True
                        
                        MDLabel:
                            text: root.report_period
                            font_style: "Body1"
                            bold: True
                            halign: "right"
                            size_hint_x: 0.7
                            adaptive_height: True

                    MDSeparator:

                    # Bagian Hasil Evaluasi
                    MDBoxLayout:
                        orientation: "vertical"
                        adaptive_height: True
                        size_hint_y: None
                        spacing: "8dp"

                        MDLabel:
                            text: "Hasil Evaluasi Guru:"
                            font_style: "Subtitle2"
                            theme_text_color: "Primary"
                            adaptive_height: True
                            size_hint_y: None
                        
                        MDLabel:
                            text: root.report_result
                            font_style: "Body1"
                            theme_text_color: "Custom"
                            text_color: 0.2, 0.2, 0.2, 1
                            adaptive_height: True
                            size_hint_y: None
                            # Line height agar lebih mudah dibaca
                            line_height: 1.2 

                # --- TOMBOL DOWNLOAD ---
                MDFillRoundFlatButton:
                    text: "DOWNLOAD PDF"
                    font_size: "16sp"
                    size_hint_x: 1
                    height: "56dp"
                    md_bg_color: 0.8, 0, 0, 1 # Merah PDF
                    on_release: root.download_pdf()
'''

Builder.load_string(KV)

class DetailLaporanOrtuScreen(Screen):
    student_name = StringProperty("-")
    student_class = StringProperty("-")
    report_period = StringProperty("-")
    report_result = StringProperty("Memuat...")
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
                self.full_report_data = hasil_dict
            except json.JSONDecodeError:
                self.report_result = data['hasil']
                self.full_report_data = None

    def download_pdf(self):
        try:
            pdf_data = {
                'nama': self.student_name,
                'kelas': self.student_class,
                'periode': self.report_period,
                'hasil': getattr(self, 'full_report_data', self.report_result),
                'guru': "Guru Wali Kelas" 
            }

            safe_name = self.student_name.replace(" ", "_")
            filename = f"Laporan_{safe_name}_{self.report_period}.pdf"
            
            filepath = ""
            if platform == 'android':
                try:
                    from android.storage import primary_external_storage_path # type: ignore
                    storage_path = primary_external_storage_path()
                    download_path = os.path.join(storage_path, 'Download')
                except:
                    download_path = "." 
                
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                filepath = os.path.join(download_path, filename)
            else:
                home = os.path.expanduser("~")
                download_path = os.path.join(home, 'Downloads')
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                filepath = os.path.join(download_path, filename)

            create_laporan_pdf(filepath, pdf_data)
            self.show_success(filepath)

        except Exception as e:
            toast(f"Gagal download: {e}")

    def show_success(self, path):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Download Berhasil",
                text=f"File tersimpan di:\n{path}",
                buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
            )
        self.dialog.text = f"File tersimpan di:\n{path}"
        self.dialog.open()

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'history_laporan'