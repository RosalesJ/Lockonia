import LockController
from Sheets import User_Sheet
from Sheets import Entry_Sheet
from itertools import chain
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.uix.behaviors.focus import FocusBehavior

class Gradient(object):

    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([ int(v * 255)  for v in chain(*args) ])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

class StartScreen(Widget):
    def on_card_tap(instance, value, label_thing):
        print(value.text)
        label_thing.text = "Welcome " + value.text
        value.select_all()
        value.delete_selection()
        value.focus = True

class Lockonia(Widget):
    pass


class LockoniaApp(App):
    def build(self):
        return StartScreen()

Builder.load_file("Lockonia.kv")

if __name__ == '__main__':
    LockoniaApp().run()
