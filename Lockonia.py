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

users = UserSheet("Lockonia_User_Sheet", 0)
log = EntrySheet("Lockonia_Log_Sheet", 0)
cameras = Sheet("Lockonia_Cameras_Sheet", 0)

blue  = (0.31640625,0.7098039216,0.8549019608,1)
white = (1, 1, 1, 1)
grey1 = (0.780, 0.780, 0.780, 1)
grey2 = (0.800, 0.800, 0.800, 1)
grey3 = (0.95, 0.95, 0.95, 1)
text_color = (0.25, 0.25, 0.25, 1)


current_user = None

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
        global current_user
        current_user = users.get_user(value.text)
        value.text = ''
        if current_user:
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

class HomeScreen(Screen):
    def goto_checkin(self):
        time.sleep(0.5)
        self.manager.current = "checkin"

    def goto_checkout(self):
        time.sleep(0.5)
        self.manager.current = "checkout"

class InvalidUserScreen(Screen):
    def on_touch_down(self, *args):
        self.manager.current = "start"

class CheckoutScreen(Screen):
    def on_touch_down(self, *args):
        Clock.schedule_once(self.done, 0.1)

    def done(self, *args):
        self.manager.current = "confirmation"

    def checkout(self, item):
        print("I checked out", item)

class CheckinScreen(Screen):
    def on_touch_down(self, *args):
        Clock.schedule_once(self.done, 0.1)

    def done(self, *args):
        self.manager.current = "confirmation"

    def checkout(self, item):
        print("I checked in", item)

class ConfirmationScreen(Screen):
     def on_touch_down(self, *args):
         self.manager.current = "start"

class LockoniaApp(App):
    def build(self):
        root = ScreenManager(transition=FadeTransition())
        root.add_widget(StartScreen())
        root.add_widget(HomeScreen())
        root.add_widget(InvalidUserScreen())
        root.add_widget(CheckoutScreen())
        root.add_widget(CheckinScreen())
        root.add_widget(ConfirmationScreen())
        return root

Builder.load_file("Lockonia.kv")

if __name__ == '__main__':
    global Lockonia
    Lockonia = LockoniaApp()
    Lockonia.run()
