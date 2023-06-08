from tkinter import *
import tkinter as tk

from scripts.audio_engine import *

class  GUI():
    '''класс графического интерфейса'''
    def __init__(self, screen_resolution='1024x768', text_speed=20, animation_speed=10, options=None):
        '''resolution - разрешение игрового окна'''

        '''создание графического окна'''
        self.options = options
        self.window = tk.Tk()
        self.window.geometry(screen_resolution) #разрешение окна
        self.window.configure(background = "white")
        self.window.wm_iconbitmap("img/icon.ico") #файл иконки
        self.window.title("Experimental game") #заголовок окна
        self.window.resizable(width=False, height=False) #запрещает менять 
                                                         #разрешение экрана
                                                         #вручную
        self.width = self.window.winfo_width()  # получаем ширину экрана
        self.height = self.window.winfo_height()  # получаем высоту экрана

        self.animation_speed = animation_speed #скорость анимации движений
        self.text_speed = text_speed
        #создаю объекты


        self.audio = AudioPlayer()
        self.audio.play('sounds/logo/logo', loop=False)
        

    def loop(self):
        '''зацикливает окно'''
        self.window.mainloop()
