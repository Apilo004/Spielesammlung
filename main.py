from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup

class GameMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        Window_x = 1000
        Window_y = 600
        Window.size = (Window_x, Window_y)

        # Button positions
        button1_pos = (200, 300)
        button2_pos = (550, 300)
        button3_pos = (200, 100)
        button4_pos = (550, 100)
        button_width = 300
        button_height = 200

        layout = FloatLayout()

        # Header
        header = BoxLayout(size_hint_y=None, height=80, pos_hint={'top': 1})
        with header.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=header.size, pos=header.pos)
            Line(rectangle=(header.x, header.y, header.width, header.height), width=2)
        header.bind(size=self._update_rect, pos=self._update_rect)
        header_label = Label(text="Spielesammlung", font_size='24sp', color=(1, 1, 1, 1))
        header.add_widget(header_label)
        layout.add_widget(header)

        # Profile button (from first example)
        profile_button = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'right': 1, 'top': 1},
            background_normal='user.png'
        )
        profile_button.bind(on_press=self.open_profile_screen)
        layout.add_widget(profile_button)

        # Game buttons
        buttons = [
            (button1_pos, "Spiel 1"),
            (button2_pos, "Spiel 2"),
            (button3_pos, "Spiel 3"),
            (button4_pos, "Spiel 4")
        ]

        for pos, text in buttons:
            button = Button(
                text=text,
                size_hint=(None, None),
                size=(button_width, button_height),
                pos=pos
            )
            button.bind(on_press=self.open_popup)
            layout.add_widget(button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_popup(self, instance):
        popup_content = Label(text="Spiel wird gestartet!")
        popup = Popup(title="Spielinfo", content=popup_content, size_hint=(0.5, 0.5))
        popup.open()

    def open_profile_screen(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'profile'

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        layout = FloatLayout()

        # Hintergrundfarbe
        with layout.canvas.before:
            Color(0.5, 0, 0.5, 1)  # Lila Hintergrund
            self.rect = Rectangle(size=(layout.width, layout.height), pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # Überschrift
        header_label = Label(
            text="Profil",
            font_size='24sp',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        layout.add_widget(header_label)

        # Eingabefelder
        username_input = TextInput(
            hint_text="Benutzername",
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        password_input = TextInput(
            hint_text="Passwort",
            password=True,
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        layout.add_widget(username_input)
        layout.add_widget(password_input)

        # Buttons
        login_button = Button(
            text="Anmelden",
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        layout.add_widget(login_button)

        regist_button = Button(
            text="Registrieren",
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.25, 'center_y': 0.3}
        )
        layout.add_widget(regist_button)

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
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'game_menu'

class MyKivyApp(App):
    def build(self):
        sm = ScreenManager()
        game_menu_screen = GameMenuScreen(name='game_menu')
        profile_screen = ProfileScreen(name='profile')
        sm.add_widget(game_menu_screen)
        sm.add_widget(profile_screen)
        return sm

if __name__ == '__main__':
    MyKivyApp().run()