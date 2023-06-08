'''это файл главного меню игры'''
from tkinter import *
import tkinter as tk
import time
import threading

from scripts.GUI.settings import *
from scripts.GUI.printer import *
from scripts.GUI.developers import *

from scripts.game_engine.act_generator import *

class MainMenu():
    '''класс отображения меню'''
    def __init__(self, window):
        '''тут используются 2 фрейма, объединенные в одном родительском фрейме.
        Это сделано для того, что бы картинка при перемещении не рвалась на 
        стыке двух фреимов. Главный фрейм - main_frame'''

        #создание фрейма меню с фоном
        self.window = window
        self.width = window.width # получаем ширину экрана
        self.height = window.height # получаем высоту экрана
        self.text_speed = int(self.window.options.text_speed)
        
        self.main_frame = tk.Frame(self.window.window) #родительский фреим
        self.settings = Settings(window, self.main_frame) #фреим настроек
        self.frame = tk.Frame(self.main_frame) #фреим гл. меню

        self.background = tk.PhotoImage(file='img/menu/menu_background.png')

        self.canvas = Canvas(self.frame, bg="white", highlightthickness=0, takefocus=1, width=self.width,  height=self.height)
        self.canvas.create_image(self.background.width()//2, self.background.height()//2, image=self.background, tag='background') #отображаю картинку лого 
        self.canvas.pack()
        self.frame.pack()
        self.settings.frame.pack()
        self.main_frame.pack()
        self.printer = Printer(self.settings.frame)
        self.about_developers = About(self.window, self.text_speed, self.canvas)

        #создание элементов управления
        #изображения кнопок
        self.new_game_unfocus = tk.PhotoImage(file='img/buttons/new_game_unfocus.png')
        self.load_game_unfocus = tk.PhotoImage(file='img/buttons/continue_unfocus.png')
        self.settings_unfocus = tk.PhotoImage(file='img/buttons/settings_unfocus.png')
        self.about_unfocus = tk.PhotoImage(file='img/buttons/about_authors_unfocus.png')
        self.quit_unfocus = tk.PhotoImage(file='img/buttons/quit_unfocus.png')

        self.new_game_focus = tk.PhotoImage(file='img/buttons/new_game_focus.png')
        self.load_game_focus = tk.PhotoImage(file='img/buttons/continue_focus.png')
        self.settings_focus = tk.PhotoImage(file='img/buttons/settings_focus.png')
        self.about_focus = tk.PhotoImage(file='img/buttons/about_authors_focus.png')
        self.quit_focus = tk.PhotoImage(file='img/buttons/quit_focus.png')

        #размещение кнопок на экране
        key_x = self.width//2
        key_y = self.height//2
        self.canvas.create_image(key_x, key_y, image=self.load_game_unfocus, tag='continue')  

        '''ТУТ НУЖНА ПРОВЕРКА, ЕСЛИ ЕСТЬ СЕЙВ, ТО ОТОБРАЗИТЬ И ЗАБИНДИТЬ continue, ЕСЛИ ЖЕ НЕТ, ТО ВЫВЕСТИ unactive'''
        
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height(), image=self.new_game_unfocus, tag='new_game') 
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height()*2, image=self.settings_unfocus, tag='settings') 
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height()*3, image=self.about_unfocus, tag='about') 
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height()*4, image=self.quit_unfocus, tag='quit') 
        

        #бинд кнопок
        self.bind()
        

    def bind(self, *args):
        '''метод биндит кнопки'''
        #тут сделать проверку, если нет начатой игры, то вывести кнопку continue_disabled, и не биндить её
        #типо if self.engine.check_saved_games:
        self.canvas.tag_bind('continue','<Enter>', self.load_game_focus_sprite)
        self.canvas.tag_bind('continue','<Leave>', self.load_game_unfocus_sprite)
        self.canvas.tag_bind('continue','<ButtonPress>', exit)

        self.canvas.tag_bind('new_game','<Enter>', self.new_game_focus_sprite)
        self.canvas.tag_bind('new_game','<Leave>', self.new_game_unfocus_sprite)
        self.canvas.tag_bind('new_game','<ButtonPress>', self.new_game)

        self.canvas.tag_bind('settings','<Enter>', self.settings_focus_sprite)
        self.canvas.tag_bind('settings','<Leave>', self.settings_unfocus_sprite)
        self.canvas.tag_bind('settings','<ButtonPress>', self.goto_settings)

        self.canvas.tag_bind('about','<Enter>', self.about_focus_sprite)
        self.canvas.tag_bind('about','<Leave>', self.about_unfocus_sprite)
        self.canvas.tag_bind('about','<ButtonPress>', self.about_developers.draw_windowbox)

        self.canvas.tag_bind('quit','<Enter>', self.quit_focus_sprite)
        self.canvas.tag_bind('quit','<Leave>', self.quit_unfocus_sprite)
        self.canvas.tag_bind('quit','<ButtonPress>', exit)

    #изменения цвета кнопок при наведении на них курсором
    def load_game_focus_sprite(self, event):
        self.canvas.itemconfigure('continue',image=self.load_game_focus)
    def load_game_unfocus_sprite(self, event):
        self.canvas.itemconfigure('continue',image=self.load_game_unfocus)
    def new_game_focus_sprite(self, event):
        self.canvas.itemconfigure('new_game',image=self.new_game_focus)
    def new_game_unfocus_sprite(self, event):
        self.canvas.itemconfigure('new_game',image=self.new_game_unfocus)
    def settings_focus_sprite(self, event):
        self.canvas.itemconfigure('settings',image=self.settings_focus)
    def settings_unfocus_sprite(self, event):
        self.canvas.itemconfigure('settings',image=self.settings_unfocus)
    def about_focus_sprite(self, event):
        self.canvas.itemconfigure('about',image=self.about_focus)
    def about_unfocus_sprite(self, event):
        self.canvas.itemconfigure('about',image=self.about_unfocus)
    def quit_focus_sprite(self, event):
        self.canvas.itemconfigure('quit',image=self.quit_focus)
    def quit_unfocus_sprite(self, event):
        self.canvas.itemconfigure('quit',image=self.quit_unfocus)


    def goto_settings(self, *args):
        '''
        метод запускает в отдельном потоке отрисовку меню-настроек
        '''
        process = threading.Thread(target=self.start)
        process.daemon = True
        process.start()

    def start(self):
        #непосредственно поток перехода в настройки
        self.window.animation_speed = int(self.window.options.animation_speed) #обновляю скорость анимации
        for i in range(0, self.height, self.window.animation_speed):
            self.draw(x=0, y=-i)
            time.sleep(0.01) #задержка обновления кадров
        self.draw(x=0, y=-self.height)


    def draw(self, x=0, y=0): 
        '''отрисовка фрейма менюшки в координатах'''
        self.main_frame.place(x=x, y=y) 

    def new_game(self, *args):
        '''клик по кнопке НОВАЯ ИГРА, тут нужна проверка, есть ли сейв, и
        если есть, то вывести окно подтверждения новой игры'''
        self.engine = ActConstructor(self.window)
        self.engine.new_game()
        self.__del__()


    def load_game(self, *args):
        '''клик по ПРОДОЛЖИТЬ'''
        pass




#-----------------------------------------------------------------------------#
    def __del__(self, *args):
        '''деструктор главного меню'''
        self.main_frame.destroy()
        self.frame.destroy()
        self.canvas.destroy()
        del self.engine
        del self.printer
        del self.about_developers
