'''при запуске игры отображает лого'''
from tkinter import *
import tkinter as tk
import time


class Logo():
    def __init__(self, window, main_menu):

        self.window = window
        self.main_menu = main_menu

        self.width = window.width  # получаем ширину экрана
        self.height = window.height  # получаем высоту экрана

        #изображения
        self.logo_image = tk.PhotoImage(file='img/logo/logo.png')
        self.present_image = tk.PhotoImage(file='img/logo/present.png')

        self.main_frame = tk.Frame(self.window.window) #основной фрейм
        self.main_frame.place(x=0, y=0)

        self.canvas = Canvas(self.main_frame, bg="white", highlightthickness=0, takefocus=1, width=self.width,  height=self.height) 
        self.canvas.pack()

        self.canvas.create_image(self.width//2, -self.logo_image.height()//2, image=self.logo_image, tag='logo') #отображаю картинку лого

        self.canvas.create_image(self.width//2, self.height+self.present_image.height(), image=self.present_image, tag='present') #отображаю картинку present


    def __del__(self):
        '''деструктор уничтожает объекты'''
        self.main_frame.destroy()
        self.canvas.destroy()


    def start(self, *args):
        '''запускает заставку игры при запуске'''       

        #движение фрейма 'Kenny games'
        for i in range(-self.logo_image.height()//2, self.height//2+self.logo_image.height()//2-self.logo_image.height()//2, 20):
            self.canvas.move('logo', 0, -self.canvas.coords('logo')[1]+i)
            time.sleep(0.01)

        # #движение фрейма 'present'
        for i in range(self.height+self.present_image.height()//2, self.height//2+(self.logo_image.height()//2), -20):
            self.canvas.move('present', 0, -self.canvas.coords('present')[1]+i)
            time.sleep(0.01)

        time.sleep(1) #задержка показa логотипа

        #логотип уезжает вправо за границы экрана, а меню выезжает слева
        for i in range(0, self.width, 20+self.window.animation_speed//2):
            self.main_frame.place(x=i)
            self.main_menu.draw(x=(-self.width)+i) #отрисовка игрового меню
            time.sleep(0.01) #задержка обновления кадров
        self.main_menu.draw(x=0, y=0)        
        self.window.audio.play('sounds/menu/background', loop=True) #запускаю мелодию менюшки
        return
