from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
# Import Model Layer (MVC) & Session
from models.user import UserModel
from models.guru import GuruModel
from config.session import set_current_user

KV = '''
<LoginScreen>:
    name: 'login'
    md_bg_color: 1, 1, 1, 1
    
    MDFloatLayout:
        # --- Logo / Icon ---
        MDIcon:
            icon: "school"
            pos_hint: {"center_x": .5, "center_y": .85}
            font_size: "60sp"
            theme_text_color: "Custom"
            text_color: 0, 0.5, 0, 1

        # --- Judul ---
        MDLabel:
            text: "Selamat Datang"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .75}
            font_style: "H5"
            bold: True
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 0.8

        MDLabel:
            text: "Silakan masuk untuk melanjutkan"
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .70}
            font_style: "Caption"
            theme_text_color: "Hint"

        # --- Form Input ---
        MDTextField:
            id: user_field
            hint_text: "Username"
            icon_right: "account"
            icon_right_color: 0, 0.5, 0, 1
            mode: "rectangle"
            pos_hint: {"center_x": .5, "center_y": .58}
            size_hint_x: .85
            line_color_focus: 0, 0.5, 0, 1

        MDTextField:
            id: pass_field
            hint_text: "Password"
            icon_right: "eye-off"
            icon_right_color: 0, 0.5, 0, 1
            mode: "rectangle"
            pos_hint: {"center_x": .5, "center_y": .46}
            size_hint_x: .85
            password: True
            line_color_focus: 0, 0.5, 0, 1
            on_icon_right: root.show_password()

        # --- Tombol Login Utama ---
        MDFillRoundFlatButton:
            id: btn_login
            text: "MASUK"
            pos_hint: {"center_x": .5, "center_y": .28}
            size_hint_x: .85
            md_bg_color: 0, 0.5, 0, 1
            font_size: "18sp"
            on_release: root.do_login()

'''

Builder.load_string(KV)

class LoginScreen(Screen):
    password_visible = False

    def show_password(self):
        """Menampilkan atau menyembunyikan password."""
        field = self.ids.pass_field
        if self.password_visible:
            field.password = True
            field.icon_right = "eye-off"
            self.password_visible = False
        else:
            field.password = False
            field.icon_right = "eye"
            self.password_visible = True

    def do_login(self):
        """Logika autentikasi menggunakan Model Layer."""
        username = self.ids.user_field.text
        password = self.ids.pass_field.text
        
        if not username or not password:
            toast("Harap isi Username dan Password!")
            return

        # Nonaktifkan tombol login agar tidak bisa ditekan berkali-kali
        self.ids.btn_login.disabled = True
        self.ids.btn_login.text = "MENGHUBUNGKAN..."

        import threading
        from kivy.clock import Clock

        def run_auth():
            try:
                # Cek koneksi db & autentikasi via thread
                user = UserModel.authenticate(username, password)
                
                # Kembalikan kontrol ke main thread
                Clock.schedule_once(lambda dt: self.on_auth_finish(user, username, password))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.on_auth_error(e))

        threading.Thread(target=run_auth, daemon=True).start()

    def on_auth_error(self, error):
        self.ids.btn_login.disabled = False
        self.ids.btn_login.text = "MASUK"
        toast("Terjadi kesalahan koneksi database!")

    def on_auth_finish(self, user, username, password):
        self.ids.btn_login.disabled = False
        self.ids.btn_login.text = "MASUK"

        if not user:
            # Periksa apakah ini karena salah password atau database memang mati
            # Jika database mati, get_db_connection() mengembalikan None
            # Kita bisa beri toast yang lebih deskriptif
            from config.database import get_db_connection
            # Coba cek apakah pool database terinisialisasi
            conn = get_db_connection()
            if not conn:
                toast("Gagal terhubung ke database. Periksa internet/Remote MySQL!")
            else:
                conn.close()
                toast("Username atau Password salah!")
            return

        # Ambal role
        role = user.get('ROLE') or user.get('role')
        user_id = user.get('id') or user.get('ID')
        
        # --- A. LOGIN GURU ---
        if role == 'Guru':
            # Ambil data guru (dijalankan di thread lain jika lambat, tapi sementara di sini)
            # Agar aman, kita fetch secara langsung
            try:
                guru_data = GuruModel.get_by_user_id(user_id)
            except Exception as e:
                toast("Gagal mengambil data guru!")
                return
            
            if guru_data:
                nama_guru = guru_data.get('nama') or guru_data.get('NAMA')
                id_guru = guru_data.get('id_guru') or guru_data.get('ID_GURU')
                
                set_current_user(
                    id_user=user_id,
                    username=user.get('username'),
                    role='Guru',
                    nama_lengkap=nama_guru,
                    id_guru=id_guru
                )
                toast(f"Selamat datang, {nama_guru}")
                self.manager.transition.direction = 'up'
                self.manager.current = 'dashboard_guru'
            else:
                toast("Data profil guru tidak ditemukan.")
        
        # --- B. LOGIN ADMIN ---
        elif role == 'Admin':
            set_current_user(
                id_user=user_id,
                username=user.get('username'),
                role='Admin',
                nama_lengkap="Administrator"
            )
            toast("Login Admin Berhasil!")
            self.manager.transition.direction = 'up'
            self.manager.current = 'dashboard_admin'
        
        # --- C. LOGIN ORANG TUA ---
        elif role == 'OrangTua':
            set_current_user(
                id_user=user_id,
                username=user.get('username'),
                role='OrangTua',
                nama_lengkap="Orang Tua Siswa"
            )
            toast("Login Orang Tua Berhasil")
            self.manager.transition.direction = 'up'
            self.manager.current = 'dashboard_ortu'
