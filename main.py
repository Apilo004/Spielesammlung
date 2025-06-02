from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
import json
import os
import sqlite3

USER_DATA_FILE = "users.json"
DB_FILE = "users.db"

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT,
            guthaben REAL DEFAULT 0,
            punkte INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password, email, guthaben, punkte):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password, email, guthaben, punkte) VALUES (?, ?, ?, ?, ?)",
            (username, password, email, guthaben, punkte)
        )
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False
    conn.close()
    return result

def check_login(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

def get_user_data(username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT username, email, guthaben, punkte FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

class GameMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        Window_x = 1000
        Window_y = 600
        Window.size = (Window_x, Window_y)

        layout = FloatLayout()

        # Set purple background
        with layout.canvas.before:
            Color(0.5, 0, 0.5, 1)  # Lila Farbe
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Header
        header = BoxLayout(size_hint_y=None, height=80, pos_hint={'top': 1})
        with header.canvas.before:
            Color(0.5, 0, 0.5, 1)
            self.header_rect = Rectangle(size=header.size, pos=header.pos)
            Line(rectangle=(header.x, header.y, header.width, header.height), width=2)
        header.bind(size=self._update_header_rect, pos=self._update_header_rect)
        header_label = Label(text="Spielesammlung", font_size='24sp', color=(1, 1, 1, 1))
        header.add_widget(header_label)
        layout.add_widget(header)

        # Profile button
        profile_button = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'right': 1, 'top': 1},
            background_normal='user-solid.png',
        )
        profile_button.bind(on_press=self.open_profile_screen)
        layout.add_widget(profile_button)

        # Options button
        options_button = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'left': 1, 'top': 1},
            background_normal='options1.png'
        )
        options_button.bind(on_press=self.open_options_screen)
        layout.add_widget(options_button)

        # Shop button
        shop_button = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'right': 0.9, 'top': 1},
            background_normal='shop.png'
        )
        shop_button.bind(on_press=self.open_shop_screen)
        layout.add_widget(shop_button)

        # Game buttons with images
        buttons = [
            ((200, 300), "spiel1.jpg"),
            ((550, 300), "spiel2.jpg"),
            ((200, 50), "spiel3.png"),
            ((550, 50), "spiel4.png")
        ]

        for pos, image in buttons:
            button = Button(
                size_hint=(None, None),
                size=(300, 200),
                pos=pos,
                background_normal=image,
                background_down=image
            )
            # Hellgrauer Rahmen um den Button, der sich anpasst
            with button.canvas.after:
                Color(0.85, 0.85, 0.85, 1)
                button.border_line = Line(rectangle=(button.x, button.y, button.width, button.height), width=3)
            def update_border(instance, value, btn=button):
                btn.border_line.rectangle = (btn.x, btn.y, btn.width, btn.height)
            button.bind(pos=update_border, size=update_border)
            button.bind(on_press=self.open_popup)
            layout.add_widget(button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _update_header_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def open_popup(self, instance):
        popup_content = Label(text="Spiel wird gestartet!")
        popup = Popup(title="Spielinfo", content=popup_content, size_hint=(0.5, 0.5))
        popup.open()

    def open_profile_screen(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'profile'

    def open_options_screen(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'options'

    def open_shop_screen(self, instance):
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'shop'

class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.5, 0, 0.5, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        header_label = Label(
            text="Optionen",
            font_size='24sp',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        layout.add_widget(header_label)

        # Sound Slider
        self.sound_slider = Slider(min=0, max=1, value=0.5, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.sound_slider.bind(value=self.change_volume)
        layout.add_widget(self.sound_slider)

        sound_label = Label(text="Lautstärke", size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.8})
        layout.add_widget(sound_label)

        # Language Dropdown
        language_dropdown = DropDown()
        for lang in ["Deutsch", "Englisch"]:
            btn = Button(text=lang, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: language_dropdown.select(btn.text))
            language_dropdown.add_widget(btn)
        language_button = Button(text="Sprache wählen", size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        language_button.bind(on_release=language_dropdown.open)
        language_dropdown.bind(on_select=lambda instance, x: setattr(language_button, 'text', x))
        layout.add_widget(language_button)

        # Window Size Dropdown
        size_dropdown = DropDown()
        for size in [("1000 x 600", (1000, 600)), ("1920 x 1080", (1920, 1080))]:
            btn = Button(text=size[0], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, s=size[1]: self.change_window_size(s))
            size_dropdown.add_widget(btn)
        size_button = Button(text="Fenstergröße wählen", size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        size_button.bind(on_release=size_dropdown.open)
        layout.add_widget(size_button)

        # Zurück-Button
        back_button = Button(
            text="Zurück",
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size    
    
    def change_volume(self, instance, value):
        print(f"Lautstärke auf {value}")

    def change_window_size(self, size):
        Window.size = size
        print(f"Fenstergröße geändert auf {size}")

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'game_menu'

class ShopScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()
    
    def build(self):
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.5, 0, 0.5, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        header_label = Label(
            text="Shop",
            font_size='24sp',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        layout.add_widget(header_label)

        back_button = Button(
            text="Zurück",
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='down')
        self.manager.current = 'game_menu'



class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = None
        self.build_login()

    def build_login(self, instance=None):
        self.clear_widgets()
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.5, 0, 0.5, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        header_label = Label(text="Anmelden", font_size='24sp', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 1})
        layout.add_widget(header_label)

        self.username_input = TextInput(hint_text="Benutzername", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.password_input = TextInput(hint_text="Passwort", password=True, size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        login_button = Button(text="Anmelden", size_hint=(0.35, 0.08), pos_hint={'center_x': 0.25, 'center_y': 0.45})
        login_button.bind(on_press=self.login)
        layout.add_widget(login_button)

        register_button = Button(text="Registrieren", size_hint=(0.35, 0.08), pos_hint={'center_x': 0.75, 'center_y': 0.45})
        register_button.bind(on_press=self.build_register)
        layout.add_widget(register_button)

        # Zurück-Button zum Homescreen
        back_button = Button(
            text="Zurück",
            size_hint=(0.35, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.18},
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        back_button.bind(on_press=self.go_home)
        layout.add_widget(back_button)

        self.info_label = Label(text="", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.35}, color=(1, 1, 1, 1))
        layout.add_widget(self.info_label)

        self.add_widget(layout)

    def build_register(self, instance=None):
        self.clear_widgets()
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.5, 0, 0.5, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        header_label = Label(text="Registrieren", font_size='24sp', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 1})
        layout.add_widget(header_label)

        self.username_input = TextInput(hint_text="Benutzername", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.password_input = TextInput(hint_text="Passwort", password=True, size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.email_input = TextInput(hint_text="E-Mail", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.guthaben_input = TextInput(hint_text="Guthaben", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.punkte_input = TextInput(hint_text="Punkte", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.3})

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.guthaben_input)
        layout.add_widget(self.punkte_input)

        register_button = Button(text="Registrieren", size_hint=(0.35, 0.08), pos_hint={'center_x': 0.25, 'center_y': 0.18})
        register_button.bind(on_press=self.register)
        layout.add_widget(register_button)

        # Zurück-Button zum Login
        back_login_button = Button(text="Zurück", size_hint=(0.35, 0.08), pos_hint={'center_x': 0.75, 'center_y': 0.18})
        back_login_button.bind(on_press=self.build_login)
        layout.add_widget(back_login_button)

        # Zusätzlicher Zurück-Button zum Homescreen
        back_home_button = Button(
            text="Home",
            size_hint=(0.35, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.08},
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        back_home_button.bind(on_press=self.go_home)
        layout.add_widget(back_home_button)

        self.info_label = Label(text="", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.1}, color=(1, 1, 1, 1))
        layout.add_widget(self.info_label)

        self.add_widget(layout)

    def build_profile(self, username):
        self.clear_widgets()
        layout = FloatLayout()
        with layout.canvas.before:
            Color(0.5, 0, 0.5, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        user = get_user_data(username)
        if user:
            uname, email, guthaben, punkte = user
            header_label = Label(text=f"Profil: {uname}", font_size='24sp', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'top': 1})
            layout.add_widget(header_label)

            email_label = Label(text=f"E-Mail: {email}", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.7})
            guthaben_label = Label(text=f"Guthaben: {guthaben}", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.6})
            punkte_label = Label(text=f"Punkte: {punkte}", size_hint=(0.8, 0.08), pos_hint={'center_x': 0.5, 'center_y': 0.5})

            layout.add_widget(email_label)
            layout.add_widget(guthaben_label)
            layout.add_widget(punkte_label)
        else:
            layout.add_widget(Label(text="Fehler: Nutzer nicht gefunden!", pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        # Back to Home button
        back_home_button = Button(
            text="Home",
            size_hint=(0.35, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.18},
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        back_home_button.bind(on_press=self.go_home)
        layout.add_widget(back_home_button)

        # Logout button
        logout_button = Button(
            text="Abmelden",
            size_hint=(0.35, 0.08),
            pos_hint={'center_x': 0.5, 'center_y': 0.08},
            background_color=(0.8, 0.2, 0.2, 1),
            background_normal=''
        )
        logout_button.bind(on_press=self.logout)
        layout.add_widget(logout_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        user = check_login(username, password)
        if user:
            self.username = username
            self.build_profile(username)
        else:
            self.info_label.text = "Falscher Benutzername oder Passwort!"
            self.info_label.color = (1, 0, 0, 1)

    def register(self, instance):
        # Diese Felder gibt es nur im Login-Layout!
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        email = self.email_input.text.strip()
        try:
            guthaben = float(self.guthaben_input.text.strip())
        except:
            guthaben = 0.0
        try:
            punkte = int(self.punkte_input.text.strip())
        except:
            punkte = 0
        if not username or not password or not email:
            self.info_label.text = "Bitte alle Felder ausfüllen!"
            self.info_label.color = (1, 0.5, 0, 1)
            return
        if register_user(username, password, email, guthaben, punkte):
            self.info_label.text = "Registrierung erfolgreich!"
            self.info_label.color = (0, 1, 0, 1)
        else:
            self.info_label.text = "Benutzer existiert bereits!"
            self.info_label.color = (1, 0.5, 0, 1)

    def logout(self, instance):
        self.username = None
        self.build_login()

    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'game_menu'

class MyKivyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameMenuScreen(name='game_menu'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(OptionsScreen(name='options'))
        sm.add_widget(ShopScreen(name='shop'))
        return sm

if __name__ == '__main__':
    init_db()
    MyKivyApp().run()
