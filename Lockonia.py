import LockController
from Sheets import UserSheet
from Sheets import EntrySheet
from itertools import chain
import time

from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


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

class CardReader(TextInput):
    def on_card_tap(instance, value):
        print(value.text)
        Clock.schedule_once(value.parent.input_detected, 0.2)

class StartScreen(Screen):
    def input_detected(instance, value):
        instance.parent.current = instance.parent.next()

class WelcomeScreen(Screen):
    def on_touch_down(instance, value):
        reader = instance.parent.screens[0].children[0]
        instance.parent.current = instance.parent.next()
        reader.focus = True

class LockoniaApp(App):
    def build(self):
        root = ScreenManager(transition=FadeTransition())
        root.add_widget(StartScreen())
        root.add_widget(WelcomeScreen())
        return root

Builder.load_file("Lockonia.kv")

if __name__ == '__main__':
    LockoniaApp().run()
