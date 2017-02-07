#import LockController
<<<<<<< HEAD
from Sheets import Sheet, UserSheet, EntrySheet, CameraSheet
=======
from Sheets import CameraSheet, UserSheet, LogSheet
>>>>>>> c77e78cfd3b1cd694586a7c1c4515ae7d0c7aac6
from User import User
from itertools import chain
import time

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

users = UserSheet("Lockonia_User_Sheet", 0)
<<<<<<< HEAD
log = EntrySheet("Lockonia_Log_Sheet", 0)
=======
log = LogSheet("Lockonia_Log_Sheet", 0)
>>>>>>> c77e78cfd3b1cd694586a7c1c4515ae7d0c7aac6
cameras = CameraSheet("Lockonia_Cameras_Sheet", 0)

active_cameras = []

blue  = (0.31640625,0.7098039216,0.8549019608,1)
white = (1, 1, 1, 1)
grey1 = (0.780, 0.780, 0.780, 1)
grey2 = (0.800, 0.800, 0.800, 1)
grey3 = (0.95, 0.95, 0.95, 1)
text_color = (0.25, 0.25, 0.25, 1)

current_user = None

def withdraw(camera):
    '''
    Withdraw a camera: verify that the camera can be withdrawn by the user, log the action, and unlock
    '''
    if cameras.withdraw_camera(camera):
        if users.update_cameras(current_user, camera, 'withdraw'):
            log.create_log('withdraw', current_user, camera)
            unlock(camera)

def deposit(camera):
    '''
    Checkout a camera: verify that the camera can be withdrawn by the user, log the action, and unlock
    '''
    if cameras.deposit_camera(camera):
        if users.update_cameras(current_user, camera, 'deposit'):
            log.create_log('deposit', current_user, camera)
            unlock(camera)

class BaseWindow(Screen):
    pass

class TopLabel(Label):
    pass

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


class HomeScreen(BaseWindow):
    def update_actions(self):
        actions = self.ids['action_buttons']
        actions.clear_widgets()
        if len(cameras.to_list()):
            actions.add_widget(Button(on_press=self.goto_checkout, background_color=blue, text='Checkout'))
        if current_user.cameras:
            actions.add_widget(Button(on_press=self.goto_checkin, background_color=blue, text='Checkin'))

            '''
            Button:
            text:"Checkout"
            on_press:root.goto_checkout()
            background_color: blue
            Button
            text:"Checkin"
            on_press:root.goto_checkin()
            background_color: blue
            '''

    def goto_checkin(self, *args):
        time.sleep(0.5)
        self.manager.current = "checkin"

    def goto_checkout(self, *args):
        time.sleep(0.5)
        self.manager.current = "checkout"

    def done(self):
        self.manager.current = 'start'


class InvalidUserScreen(Screen):
    def on_touch_down(self, *args):
        self.manager.current = "start"


class CheckoutScreen(Screen):
    def done(self, *args):
        self.manager.current = "confirmation"

    def checkout(self, camera):
        print("I checked out", camera)
        Clock.schedule_once(self.done, 0.1)

    def back(self):
        self.manager.current = 'welcome'

    def update_displayed_cameras(self):
        displayed_cameras = self.ids['displayed_cameras']
        displayed_cameras.clear_widgets()
        for camera in cameras.to_list():
            displayed_cameras.add_widget(Button(text=camera, id=camera, background_color=blue))


class CheckinScreen(Screen):
    def done(self, *args):
        self.manager.current = "confirmation"

    def checkin(self, camera):
        print("I checked in", camera)
        Clock.schedule_once(self.done, 0.1)

    def back(self):
        self.manager.current = 'welcome'

    def update_displayed_cameras(self):
        displayed_cameras = self.ids['displayed_cameras']
        displayed_cameras.clear_widgets()
        user_cameras = current_user.cameras
        for camera in user_cameras:
            displayed_cameras.add_widget(Button(text=camera, id=camera, background_color=blue))



class ConfirmationScreen(Screen):
     def on_touch_down(self, *args):
         self.manager.current = "welcome"


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
