from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.storage.jsonstore import JsonStore

KV = '''
<OnboardingScreen>:
    name: 'onboarding'
    md_bg_color: 1, 1, 1, 1

    MDFloatLayout:
        MDCarousel:
            id: carousel
            direction: 'right'
            on_slide_complete: root.on_slide_change(self)

            # --- SLIDE 1 ---
            MDFloatLayout:
                # Ganti source gambar jika sudah ada asset
                # Image:
                #    source: "assets/images/onboard1.png"
                #    pos_hint: {"center_x": .5, "center_y": .6}
                #    size_hint: .5, .5
                
                MDIcon:
                    icon: "notebook-edit"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    font_size: "100sp"
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.6, 0.8, 1
                MDLabel:
                    text: "Pencatatan Mudah"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    halign: "center"
                    font_style: "H4"
                    bold: True
                MDLabel:
                    text: "Input nilai perkembangan anak secara digital,\\ncepat, dan terorganisir."
                    pos_hint: {"center_x": .5, "center_y": .3}
                    halign: "center"
                    font_style: "Body1"
                    color: 0.5, 0.5, 0.5, 1

            # --- SLIDE 2 ---
            MDFloatLayout:
                MDIcon:
                    icon: "chart-bar"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    font_size: "100sp"
                    theme_text_color: "Custom"
                    text_color: 0.8, 0.4, 0.2, 1
                MDLabel:
                    text: "Analisa Otomatis"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    halign: "center"
                    font_style: "H4"
                    bold: True
                MDLabel:
                    text: "Algoritma Rule-Based mengolah nilai harian\\nmenjadi status perkembangan (BSB, BSH) instan."
                    pos_hint: {"center_x": .5, "center_y": .3}
                    halign: "center"
                    font_style: "Body1"
                    color: 0.5, 0.5, 0.5, 1

            # --- SLIDE 3 ---
            MDFloatLayout:
                MDIcon:
                    icon: "file-document-outline"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    font_size: "100sp"
                    theme_text_color: "Custom"
                    text_color: 0.2, 0.8, 0.4, 1
                MDLabel:
                    text: "Laporan Real-time"
                    pos_hint: {"center_x": .5, "center_y": .4}
                    halign: "center"
                    font_style: "H4"
                    bold: True
                MDLabel:
                    text: "Pantau hasil belajar dan unduh laporan\\nperkembangan anak kapan saja."
                    pos_hint: {"center_x": .5, "center_y": .3}
                    halign: "center"
                    font_style: "Body1"
                    color: 0.5, 0.5, 0.5, 1

        # Indikator Dots
        MDBoxLayout:
            pos_hint: {"center_x": .5, "center_y": .18}
            size_hint: .2, .05
            spacing: "10dp"
            halign: "center"
            
            MDIcon:
                id: dot1
                icon: "circle"
                font_size: "10sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
            MDIcon:
                id: dot2
                icon: "circle-outline"
                font_size: "10sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
            MDIcon:
                id: dot3
                icon: "circle-outline"
                font_size: "10sp"
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1

        # Tombol Navigasi
        MDFillRoundFlatButton:
            id: btn_next
            text: "LANJUT"
            pos_hint: {"right": .9, "y": .05}
            on_release: root.next_slide()
            md_bg_color: 0, 0.5, 0, 1

        MDTextButton:
            text: "LEWATI"
            pos_hint: {"x": .1, "y": .065}
            theme_text_color: "Custom"
            text_color: 0.5, 0.5, 0.5, 1
            on_release: root.skip_onboarding()
'''

Builder.load_string(KV)

class OnboardingScreen(Screen):
    def next_slide(self):
        carousel = self.ids.carousel
        current_slide = carousel.index
        
        if current_slide < 2:
            carousel.load_slide(carousel.slides[current_slide + 1])
        else:
            self.finish_onboarding()

    def skip_onboarding(self):
        self.finish_onboarding()

    def finish_onboarding(self):
        store = JsonStore('app_config.json')
        store.put('onboarding', completed=True)
        self.manager.transition.direction = 'left'
        self.manager.current = 'login'

    def on_slide_change(self, carousel_instance):
        index = carousel_instance.index
        self.ids.dot1.icon = "circle-outline"
        self.ids.dot2.icon = "circle-outline"
        self.ids.dot3.icon = "circle-outline"
        
        if index == 0:
            self.ids.dot1.icon = "circle"
            self.ids.btn_next.text = "LANJUT"
        elif index == 1:
            self.ids.dot2.icon = "circle"
            self.ids.btn_next.text = "LANJUT"
        elif index == 2:
            self.ids.dot3.icon = "circle"
            self.ids.btn_next.text = "MULAI SEKARANG"