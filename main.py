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
            background_normal='user.png'
        )
        profile_button.bind(on_press=self.open_profile_screen)
        layout.add_widget(profile_button)

        # Options button
        options_button = Button(
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={'left': 1, 'top': 1},
            background_normal='options.png'
        )
        options_button.bind(on_press=self.open_options_screen)
        layout.add_widget(options_button)

        # Game buttons
        buttons = [
            ((200, 300), "Spiel 1"),
            ((550, 300), "Spiel 2"),
            ((200, 50), "Spiel 3"),
            ((550, 50), "Spiel 4")
        ]

        for pos, text in buttons:
            button = Button(
                text=text,
                size_hint=(None, None),
                size=(300, 200),
                pos=pos
            )
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
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'game_menu'

class ProfileScreen(Screen):
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
            text="Profil",
            font_size='24sp',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 1}
        )
        layout.add_widget(header_label)

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
        sm.add_widget(GameMenuScreen(name='game_menu'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(OptionsScreen(name='options'))
        return sm

if __name__ == '__main__':
    MyKivyApp().run()
