from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from models.penilaian import PenilaianModel
from models.anekdot import AnekdotModel
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

def convert_nilai_to_huruf(nilai_angka):
    teks = {1: "BB", 2: "MB", 3: "BSH", 4: "BSB"}
    return teks.get(nilai_angka, "-")

KV = '''
<KartuPerkembangan>:
    orientation: "vertical"
    padding: "16dp"
    spacing: "8dp"
    size_hint_y: None
    height: self.minimum_height
    radius: [16]
    elevation: 2
    md_bg_color: 1, 1, 1, 1
    
    MDBoxLayout:
        adaptive_height: True
        orientation: "horizontal"
        
        MDLabel:
            text: root.tgl
            font_style: "Caption"
            theme_text_color: "Secondary"
            
        MDBoxLayout:
            adaptive_size: True
            padding: ["8dp", "2dp", "8dp", "2dp"]
            md_bg_color: root.badge_color
            radius: [8]
            
            MDLabel:
                text: root.nilai_huruf
                font_style: "Caption"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                halign: "center"
                
    MDLabel:
        text: root.indikator
        font_style: "Subtitle2"
        bold: True
        theme_text_color: "Primary"
        adaptive_height: True
        
    MDLabel:
        text: root.catatan if root.catatan else "Belum ada catatan khusus."
        font_style: "Body2"
        theme_text_color: "Custom"
        text_color: 0.3, 0.3, 0.3, 1
        adaptive_height: True

<KartuAnekdot>:
    orientation: "vertical"
    padding: "16dp"
    spacing: "8dp"
    size_hint_y: None
    height: self.minimum_height
    radius: [16]
    elevation: 2
    md_bg_color: 0.95, 0.98, 1.0, 1  # Biru muda soft untuk pembeda
    
    MDBoxLayout:
        adaptive_height: True
        orientation: "horizontal"
        
        MDLabel:
            text: root.tgl
            font_style: "Caption"
            theme_text_color: "Secondary"
            
        MDLabel:
            text: "Catatan Guru"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.25, 0.47, 0.85, 1
            bold: True
            halign: "right"
            
    MDLabel:
        text: root.catatan
        font_style: "Body2"
        theme_text_color: "Primary"
        adaptive_height: True
        
    MDLabel:
        text: "Oleh: " + root.guru
        font_style: "Caption"
        italic: True
        theme_text_color: "Secondary"
        adaptive_height: True

<PerkembanganAnakOrtuScreen>:
    name: 'perkembangan_anak_ortu'
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
                text: "Perkembangan Ananda"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                pos_hint: {"center_y": .5}

        # TAB SELECTOR (Simple)
        MDBoxLayout:
            size_hint_y: None
            height: "48dp"
            md_bg_color: 1, 1, 1, 1
            padding: "4dp"
            
            MDFlatButton:
                id: btn_tab_nilai
                text: "Nilai Harian"
                size_hint_x: 0.5
                theme_text_color: "Custom"
                text_color: (0.91, 0.45, 0.14, 1) if root.tab_active == 'nilai' else (0.5, 0.5, 0.5, 1)
                on_release: root.switch_tab('nilai')
                
            MDFlatButton:
                id: btn_tab_anekdot
                text: "Catatan Guru"
                size_hint_x: 0.5
                theme_text_color: "Custom"
                text_color: (0.91, 0.45, 0.14, 1) if root.tab_active == 'anekdot' else (0.5, 0.5, 0.5, 1)
                on_release: root.switch_tab('anekdot')

        # CONTENT
        ScrollView:
            MDBoxLayout:
                id: list_content
                orientation: "vertical"
                padding: "20dp"
                spacing: "16dp"
                adaptive_height: True
'''

Builder.load_string(KV)

class KartuPerkembangan(MDCard):
    tgl = StringProperty("")
    indikator = StringProperty("")
    nilai_huruf = StringProperty("")
    catatan = StringProperty("")
    badge_color = (0.5, 0.5, 0.5, 1)

class KartuAnekdot(MDCard):
    tgl = StringProperty("")
    catatan = StringProperty("")
    guru = StringProperty("")

class PerkembanganAnakOrtuScreen(Screen):
    id_siswa = None
    tab_active = StringProperty("nilai")

    def set_siswa(self, id_siswa):
        self.id_siswa = id_siswa

    def on_enter(self):
        self.load_data()

    def switch_tab(self, tab):
        self.tab_active = tab
        self.load_data()

    def load_data(self):
        self.ids.list_content.clear_widgets()
        
        if not self.id_siswa:
            return
            
        if self.tab_active == 'nilai':
            self.load_nilai()
        else:
            self.load_anekdot()

    def load_nilai(self):
        details = PenilaianModel.get_details_by_siswa(self.id_siswa)
        
        if not details:
            from kivymd.uix.label import MDLabel
            self.ids.list_content.add_widget(
                MDLabel(text="Belum ada data penilaian.", halign="center", theme_text_color="Hint", padding=[0, 50, 0, 0])
            )
            return

        for d in details:
            huruf = convert_nilai_to_huruf(d['nilai'])
            if huruf == 'BSB': color = (0.13, 0.55, 0.33, 1)
            elif huruf == 'BSH': color = (0.25, 0.47, 0.85, 1)
            elif huruf == 'MB': color = (0.91, 0.65, 0.14, 1)
            else: color = (0.8, 0.2, 0.2, 1)
            
            card = KartuPerkembangan(
                tgl=d['tgl'].strftime('%d %b %Y') if hasattr(d['tgl'], 'strftime') else str(d['tgl']),
                indikator=d['indikator'],
                nilai_huruf=huruf,
                catatan=d.get('catatan') or "",
            )
            card.badge_color = color
            self.ids.list_content.add_widget(card)

    def load_anekdot(self):
        anekdots = AnekdotModel.get_by_siswa(self.id_siswa)
        
        if not anekdots:
            from kivymd.uix.label import MDLabel
            self.ids.list_content.add_widget(
                MDLabel(text="Belum ada catatan anekdot dari guru.", halign="center", theme_text_color="Hint", padding=[0, 50, 0, 0])
            )
            return

        for a in anekdots:
            card = KartuAnekdot(
                tgl=a['tanggal'].strftime('%d %b %Y') if hasattr(a['tanggal'], 'strftime') else str(a['tanggal']),
                catatan=a['catatan'],
                guru=a['nama_guru'] or "Guru Pengajar"
            )
            self.ids.list_content.add_widget(card)

    def kembali(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard_ortu'
