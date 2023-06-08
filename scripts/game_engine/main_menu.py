'''это файл главного меню игры, вызываемый при нажатии ESCAPE во время игры'''
from tkinter import *
import tkinter as tk
import time
import threading

from scripts.GUI.settings import *
from scripts.GUI.printer import *
from scripts.GUI.developers import *


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

        self.pause = False #флаг, что игра на паузе
        
        self.main_frame = tk.Frame(self.window.window) #родительский фреим
        self.settings = Settings(window, self.main_frame) #фреим настроек
        self.frame = tk.Frame(self.main_frame) #фреим гл. меню

        self.background = tk.PhotoImage(file='img/menu/menu_background.png')

        self.canvas = Canvas(self.frame, bg="white", highlightthickness=0, takefocus=1, width=self.width,  height=self.height)
        self.canvas.create_image(self.background.width()//2, self.background.height()//2, image=self.background, tag='background') #отображаю картинку лого 
        self.canvas.pack()
        self.frame.pack()
        self.settings.frame.pack() 
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
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height(), image=self.new_game_unfocus, tag='new_game') 
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height()*2, image=self.settings_unfocus, tag='settings') 
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height()*3, image=self.about_unfocus, tag='about') 
        self.canvas.create_image(key_x, key_y+self.load_game_unfocus.height()*4, image=self.quit_unfocus, tag='quit') 


        

    def bind(self, *args):
        '''метод биндит кнопки'''
        self.canvas.tag_bind('continue','<Enter>', self.load_game_focus_sprite)
        self.canvas.tag_bind('continue','<Leave>', self.load_game_unfocus_sprite)
        self.canvas.tag_bind('continue','<ButtonPress>', self.hide)

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

        self.frame.focus()
        self.frame.bind('<Key-Escape>', self.hide)

    def unbind_all(self, *args):
        self.frame.unbind('<Key-Escape>')
        self.frame.unfocus()

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


    def new_game(self, *args):
        '''клик по кнопке НОВАЯ ИГРА. Нужно вывести окно подтверждения новой игры'''
        self.new_game_windowbox = tk.PhotoImage(file='img/menu/new_game_windowbox.png')
        self.new_game_yes_unfocus = tk.PhotoImage(file='img/menu/new_game_yes_unfocus.png')
        self.new_game_yes_focus = tk.PhotoImage(file='img/menu/new_game_yes_focus.png')
        self.new_game_no_unfocus = tk.PhotoImage(file='img/menu/new_game_no_unfocus.png')
        self.new_game_no_focus = tk.PhotoImage(file='img/menu/new_game_no_focus.png')

        self.canvas.create_image(self.width//2, self.height//2, image=self.new_game_windowbox, tag='new_game_windowbox')  
        
        x = ((self.width//2)-(self.new_game_windowbox.width()//2)+tk.PhotoImage(file='img/font/space.png').width()*2)
        y = self.height//2-int((self.new_game_windowbox.height()//2))+tk.PhotoImage(file='img/font/space.png').height()+(tk.PhotoImage(file='img/font/space.png').height()//2)
        max_in_line = self.new_game_windowbox.width()//tk.PhotoImage(file='img/font/space.png').width()-3
        max_lines = self.new_game_windowbox.height()//tk.PhotoImage(file='img/font/space.png').height()
        self.new_game_printer = Printer(self.settings.frame)
        thread = threading.Thread(target=self.new_game_printer.print, args=('Вы действительно хотите начать новую игру? Сохранения будут утеряны!', x, y, max_in_line, max_lines, True, self.canvas, False))
        thread.daemon = True
        thread.start()
        #размещаю кнопки ДА/НЕТ на экране
        self.canvas.create_image(self.width//2-self.new_game_windowbox.width()//4, self.height//2+self.new_game_windowbox.height()//4, image=self.new_game_yes_unfocus, tag='new_game_yes')
        self.canvas.create_image(self.width//2+self.new_game_windowbox.width()//4, self.height//2+self.new_game_windowbox.height()//4, image=self.new_game_no_unfocus, tag='new_game_no')
        #
        self.canvas.tag_bind('new_game_yes','<Enter>', self.yes_focus)
        self.canvas.tag_bind('new_game_yes','<Leave>', self.yes_unfocus)
        self.canvas.tag_bind('new_game_yes','<ButtonPress>', self.start_new_game)
        self.canvas.tag_bind('new_game_no','<Enter>', self.no_focus)
        self.canvas.tag_bind('new_game_no','<Leave>', self.no_unfocus)
        self.canvas.tag_bind('new_game_no','<ButtonPress>', self.destroy_new_game_windowbox)
        #
    def yes_focus(self, *args):
        self.canvas.itemconfigure('new_game_yes',image=self.new_game_yes_focus)
    def yes_unfocus(self, *args):
        self.canvas.itemconfigure('new_game_yes',image=self.new_game_yes_unfocus)
    def no_focus(self, *args):
        self.canvas.itemconfigure('new_game_no',image=self.new_game_no_focus)
    def no_unfocus(self, *args):
        self.canvas.itemconfigure('new_game_no',image=self.new_game_no_unfocus)

    def start_new_game(self, *args):
        self.pause = 'new_game'
        self.hide()

    def destroy_new_game_windowbox(self, *args):
        '''удаляет рамку новой игры при нажатии на нет'''
        self.canvas.delete('new_game_yes')
        self.canvas.delete('new_game_no')
        self.canvas.delete('new_game_windowbox')
        self.new_game_printer.clear()
        del self.new_game_printer

    def draw(self, x=0, y=0): 
        '''отрисовка фрейма менюшки в координатах'''
        self.main_frame.place(x=x, y=y) 
        if self.pause == 'new_game':
            pass
        else:
            self.pause = True

    def hide(self, *args):
        '''при нажатии на ПРОДОЛЖИТЬ или НОВАЯ ИГРА скрывает меню'''
        try:
            self.destroy_new_game_windowbox()
        except:
            pass
        self.draw(x=self.width, y=self.height)
        if self.pause == 'new_game':
            pass
        else:
            self.pause = False
            