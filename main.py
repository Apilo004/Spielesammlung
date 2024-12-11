from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyKivyApp(App):
    def build(self):
        # Layout erstellen
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Label hinzufügen
        self.label = Label(text="Drücke den Button", font_size='20sp')
        layout.add_widget(self.label)

        # Button hinzufügen
        button = Button(text="Klick mich!", font_size='20sp', size_hint=(1, 0.2))
        button.bind(on_press=self.on_button_press)
        layout.add_widget(button)

        return layout

    def on_button_press(self, instance):
        # Aktion, wenn der Button gedrückt wird
        self.label.text = "Der Button wurde gedrückt!"

# App starten
if __name__ == "__main__":
    MyKivyApp().run()