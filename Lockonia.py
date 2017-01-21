#import LockController
from Sheets import Sheet, UserSheet, EntrySheet
from User import User
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

UserSheet = UserSheet("Lockonia_User_Sheet", 0)
EntrySheet = EntrySheet("Lockonia_Log_Sheet", 0)
CameraSheet = Sheet("Lockonia_Cameras_Sheet", 0)

CurrentUser = None

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
        global CurrentUser
        CurrentUser = UserSheet.get_user(value.text)
        print(value.text)
        value.text = ''
        if CurrentUser:
            Clock.schedule_once(value.parent.welcome_user, 0.2)
        else:
            Clock.schedule_once(value.parent.invalid_user, 0.2)

class StartScreen(Screen):
    def welcome_user(self, *args):
        self.manager.current = "welcome"

    def invalid_user(self, *args):
        self.manager.current = "invalid_user"

    def focus_card_reader(self, card_reader):
        card_reader.focus = True

class WelcomeScreen(Screen):
    def on_touch_down(self, *args):
        self.manager.current = "start"

class InvalidUserScreen(Screen):
    def on_touch_down(self, *args):
        self.manager.current = "start"

class LockoniaApp(App):
    def build(self):
        root = ScreenManager(transition=FadeTransition())
        root.add_widget(StartScreen())
        root.add_widget(WelcomeScreen())
        root.add_widget(InvalidUserScreen())
        return root

Builder.load_file("Lockonia.kv")

if __name__ == '__main__':
    global Lockonia
    Lockonia = LockoniaApp()
    Lockonia.run()
