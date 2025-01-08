from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line

class MyKivyApp(App):
    def build(self):
        # Fenstergröße einstellen
        Window.size = (800, 600)

        # Layout erstellen
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Überschrift hinzufügen
        header = BoxLayout(size_hint_y=None, height=100)
        with header.canvas.before:
            Color(0, 0, 0, 1)  # Schwarz
            self.rect = Rectangle(size=header.size, pos=header.pos)
            Line(rectangle=(header.x, header.y, header.width, header.height), width=2)
        header.bind(size=self._update_rect, pos=self._update_rect)
        header_label = Label(text="Spielesammlung", font_size='24sp', color=(1, 1, 1, 1))
        header.add_widget(header_label)
        layout.add_widget(header)

        # Buttons in einem 2x2 Block hinzufügen
        button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=150)
        left_column = BoxLayout(orientation='vertical', spacing=10)
        right_column = BoxLayout(orientation='vertical', spacing=10)

        for i in range(2):
            left_column.add_widget(Button(text=f"Button {i*2+1}", size_hint=(1, 1)))
            right_column.add_widget(Button(text=f"Button {i*2+2}", size_hint=(1, 1)))

        button_layout.add_widget(left_column)
        button_layout.add_widget(right_column)

        # Buttons unter die Überschrift platzieren
        layout.add_widget(button_layout)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# App starten
if __name__ == "__main__":
    MyKivyApp().run()