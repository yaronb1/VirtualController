import os
import SmartController as sm

import pickle

import cv2
import numpy as np
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config

Config.set('graphics', 'resizable', True)
Builder.load_file('UIApp.kv')

project_folder = '/home/yaron/PycharmProjects/SmartController/'

ges_images_folder = '/home/yaron/PycharmProjects/SmartController/images/ges_images'
ges_images = os.listdir(ges_images_folder)
global screenM
w,h = 1280,720

class Main(Screen):

    def new_screen(self):

        cam =  CamApp()
        s = cam.build()
        self.add_widget(s)


        print('yes')

class NewScreen(Screen):
    ges_ui = 'fdfd'
    btn_ui = ''
    background = []
    x_ = 0
    y_ = 0
    gestures = []

    def build(self):

        self.add_image()
        self.create_ges_menu()
        self.image_creator = sm.simpleUI()
        #self.create_menu('Button')

    def add_image(self):
        cam = CamApp()
        lay = cam.build()
        self.ids['image'].add_widget(lay)
        #

    def create_ges_menu(self):
        ges_dropdown = UIModeSelect()
        ges_mainbutton = Button(text='Gesture', size_hint=(None, None))
        ges_mainbutton.bind(on_release=ges_dropdown.open)
        ges_dropdown.bind(on_select=lambda instance, x: setattr(ges_mainbutton, 'background_normal', x))
        ges_dropdown.bind(on_select=lambda instance, x: setattr(ges_mainbutton, 'text', ''))
        for index in ges_images:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            btn = Button(#text='Value %d' % index,
                 background_normal= ges_images_folder + '/' +str(index),  size_hint_y=None, height=74)

            #print(index)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            #btn.bind(on_release=lambda btn: ges_dropdown.select(btn.text))
            btn.bind(on_release=lambda btn: ges_dropdown.select(btn.background_normal))
            print(btn.background_normal)
            btn.bind(on_release=lambda btn: self.btn_bind(btn.background_normal))

            # then add the button inside the dropdown
            ges_dropdown.add_widget(btn)


        ges_dropdown.dismiss()

        func_dropdown = UIModeSelect()
        func_mainbutton = Button(text='func', size_hint=(None, None))
        func_mainbutton.bind(on_release=func_dropdown.open)
        func_dropdown.bind(on_select=lambda instance, x: setattr(func_mainbutton, 'text', x))
        #func_dropdown.bind(on_select=lambda instance, x: setattr(func_mainbutton, 'background_normal', x))
        for index in range(10):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            btn = Button(text='Value %d' % index, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: func_dropdown.select(btn.text))

            # then add the button inside the dropdown
            func_dropdown.add_widget(btn)
        func_dropdown.dismiss()

        # add_func_btn = Button(text = 'add Gesture', size_hint=(None,None))
        # add_ui_btn = Button(text='add UI', size_hint=(None, None))
        # add_ui_btn.bind(on_release= self.add_ui )

        self.ids['menu'].add_widget(ges_dropdown)
        self.ids['menu'].add_widget(ges_mainbutton)

        self.ids['menu'].add_widget(func_dropdown)
        self.ids['menu'].add_widget(func_mainbutton)

        #self.ids['menu'].add_widget(add_func_btn)
        #self.ids['menu'].add_widget(add_ui_btn)

    def add_ges(self):
        self.add_ui()

        if self.ges_to_add == 1:
            ges = [0,1,0,0,0]
        elif self.ges_to_add == 2:
            ges=[0,1,1,0,0]
        elif self.ges_to_add == 3:
            ges=[0,1,1,1,0]
        elif self.ges_to_add == 4:
            ges = [0,1,1,1,1]
        else:
            print('error getting gesture')
            return

        self.gestures.append(ges)



    def add_ui(self):
        print(self.ges_ui)
        img = cv2.imread(self.ges_ui)

        try:self.background = self.image_creator.add_image_to_background(img,(300,200),(h,w), x= self.x_*300, y=self.y_*200)
        except:
            self.x_=0
            self.y_ +=1
            try:self.background = self.image_creator.add_image_to_background(img,(300,200),(h,w), x= self.x_*300, y=self.y_*200)
            except Exception as e:
                print('screen out of room')
                print(e)
            else: self.x_+=1
        else:
            self.x_+=1

    def btn_bind(self, text):
        self.ges_ui= text
        print(text[62])
        self.ges_to_add = int(text[62])

    def save_screen(self):
        screen_name = self.ids['screen_name'].text
        path = self.create_folder(screen_name)
        #file = ges_images_folder[:50] + '/screen_images/' + screen_name + '.png'
        file = path + '/' + screen_name + '_background.png'
        cv2.imwrite(file, self.background)
        print('image saved to ' + str(file))
        print(self.gestures)
        with open(path + '/variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump(self.gestures, f)

    def create_folder(self, folder_name):
        path = os.path.join(project_folder + '/custom_screens', str(folder_name) + '_screen')
        os.mkdir(path)
        return path

    def get_variables(self):
        # Getting back the objects:
        with open('/home/yaron/PycharmProjects/SmartController/variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
            gestures = pickle.load(f)

        print(gestures)




class UIModeSelect(DropDown):
    pass

class TestApp(App):
    def build(self):
        global screenM
        screenM = ScreenManager()

        screenM.add_widget(Main(name='Main'))
        screenM.add_widget(NewScreen(name= 'NewScreen'))
        return screenM


class CamApp(Widget):

    start = True
    def build(self):
        self.img1=Image()

        self.image_creator = sm.simpleUI()
        #self.tranparent_background = self.image_creator.create_transparent_backround(size=self.img1.size)

        layout = BoxLayout()
        layout.add_widget(self.img1)
        #print('image added')
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3,w)
        self.capture.set(4,h)
        #cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)


        #print(self.img1.size)

        return layout

    def add_ui_image(self, img_path):
        img = cv2.imread(img_path)
        self.tranparent_background =  self.image_creator.add_image_to_background(img, (320,200), None)



    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()


        frame1 = self.cv_funcs(frame)
        #cv2.imshow("CV2 Image", frame1)
        #cv2.waitKey(1)
        # convert it to texture
        buf1 = cv2.flip(frame1, 0)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        #texture1.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')# for grayscale
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte') # for color
        # display image from the texture
        self.img1.texture = texture1

    def cv_funcs(self, frames):

        #print(screenM.children[0].ui_images)
        background = screenM.children[0].background
        try:final = sm.Controller().overlay_transparent(frames, background, 0, 0)
        except Exception as e:
            return frames
        else:return final


if __name__ == "__main__":

    TestApp().run()

    #CamApp().run()
    # ui_creator = sm.simpleUI()
    # ui_size = (320,200)
    # background_size = (1280, 720)
    #
    #
    # img = cv2.imread(ges_images_folder + '/' + str(ges_images[0]))
    #
    #
    # img_overlay = ui_creator.add_image_to_background(img,ui_size, background_size)
    # cap = cv2.VideoCapture(0)
    #
    # success, vid = cap.read()
    # vid = cv2.resize(vid, background_size)
    #
    # cv2.imshow('vid', vid)
    # cv2.imshow('img',img)
    #
    # final = sm.Controller().overlay_transparent(vid, img_overlay,0,0)
    #
    # cv2.imshow('final', final)
    #
    #
    # cv2.waitKey(0)
    #
    # img = cv2.imread(ges_images_folder + '/' + str(ges_images[1]))
    # img_overlay = ui_creator.add_image_to_background(img, ui_size, background_size, x=400)
    #
    # cv2.imshow('vid', vid)
    # cv2.imshow('img',img)
    #
    # final = sm.Controller().overlay_transparent(vid, img_overlay,0,0)
    #
    # cv2.imshow('final', final)
    #
    # cv2.waitKey(0)





