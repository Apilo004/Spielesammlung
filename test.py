from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.floatlayout import FloatLayout

class MyKivyApp(App):

    def build(self):
        
        Window_x = 1000
        Window_y = 600

        # Window size
        Window.size = (Window_x, Window_y)

        # Button position variables
        button1_pos = (200, 300)  # (x, y) for button 1
        button2_pos = (550, 300)  # (x, y) for button 2
        button3_pos = (200, 100)  # (x, y) for button 3
        button4_pos = (550, 100)  # (x, y) for button 4
        
        # Button size variables
        button_width = 300
        button_height = 200

        # Main layout
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

        # Create buttons with absolute positioning
        buttons = [
            (button1_pos, "Button 1"),
            (button2_pos, "Button 2"),
            (button3_pos, "Button 3"),
            (button4_pos, "Button 4")
        ]

        for pos, text in buttons:
            button = Button(
                text=text,
                size_hint=(None, None),
                size=(button_width, button_height),
                pos=pos
            )
            layout.add_widget(button)

        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# Start app
if __name__ == "__main__":
    MyKivyApp().run()