from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle


class MyKivyApp(App):
    def build(self):
        # Hauptlayout
        layout = FloatLayout()

        # Hintergrundfarbe setzen
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Weißer Hintergrund
            self.rect = Rectangle(size=(layout.width, layout.height), pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)

        # User-Icon als Bild oben rechts platzieren (proportional)
        user_image = Image(
            source='user.jpg',
            size_hint=(0.1, 0.1),
            pos_hint={'right': 1, 'top': 1},
            allow_stretch=False,  # Proportional anzeigen
            keep_ratio=True
        )
        layout.add_widget(user_image)

        # Unsichtbarer Button über dem Bild für die Klickfunktion
        image_button = Button(
            size_hint=(0.1, 0.1),
            pos_hint={'right': 1, 'top': 1},
            background_color=(0, 0, 0, 0)  # Unsichtbarer Button
        )
        image_button.bind(on_press=self.open_popup)
        layout.add_widget(image_button)

        # Button in die Mitte platzieren
        button = Button(text="Klick mich!", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        button.bind(on_press=self.open_popup)
        layout.add_widget(button)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def open_popup(self, instance):
        # Popup erstellen
        popup_content = Label(text="Hier ist dein Popup!")
        popup = Popup(title="User Info", content=popup_content, size_hint=(0.5, 0.5))
        popup.open()


if __name__ == '__main__':
    MyKivyApp().run()
