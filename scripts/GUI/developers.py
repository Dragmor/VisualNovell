from tkinter import *
import tkinter as tk
import threading
import time

from scripts.GUI.printer import *

class About():
    '''класс реализует вывод на экран информации о разработчиках
    
        МЕТОДЫ КЛАССА:
    self.window.about_developers.draw_windowbox() #запускает окно отображения
    self.window.about_developers.stop()  #закрывает окно

    #'\': #символ, используемый для переноса строки!
    #'^': используется, если нужно подряд несколько пробелов
    '''

    def __init__(self, window, text_speed=20, canvas=None):
        self.window = window
        self.canvas = canvas
        self.text_speed = 0.3/text_speed #скорость вывода текста
        self.width = window.window.winfo_width()
        self.height = window.window.winfo_height()
        file = open('text/developers', 'r') #файл с текстом о разработчиках
        self.text = file.read() #файл с текстом о разработчиках
        file.close()
        self.printer = Printer(self.window.window)

    def bind_keys(self):
        '''метод биндит кнопки'''
        self.canvas.focus('developers_windowbox')
        self.canvas.tag_bind('developers_windowbox','<ButtonPress>', self.mouse_clicked)

        self.window.window.focus()
        self.window.window.bind('<KeyPress>', self.key_processing)


    def draw_windowbox(self, *args):
        '''метод рисует рамку, в которой будет выводится текст'''
        self.windowbox_img = tk.PhotoImage(file='img/menu/developers_windowbox.png') #изображение рамки для текста
        self.canvas.create_image((self.width-self.windowbox_img.width())//2+self.windowbox_img.width()//2, (self.height-self.windowbox_img.height())//2+self.windowbox_img.height()//2, image=self.windowbox_img, tag='developers_windowbox')
        self.start()

    def key_processing(self, button):
        '''метод обрабатывает нажатия клавиш'''
        if button.keycode == 32 or button.keycode == 13: #нажат пробел или ентер
            if self.printer.backrolling(): #проматываю текст. Если он уже проматывается, и снова нажат пробел, закрываю окно вывода текста
                self.stop()
        elif button.keycode == 27: #если нажат ескейп
            self.stop() #закрываю окно 'авторы'

    def mouse_clicked(self, *args):
        '''если нажата кнопка мыши, проматываю текстю Если уже проматывается,
        закрываю окно вывода текста'''
        if self.printer.backrolling(): #проматываю текст. 
            self.stop() #Если он уже проматывается, и снова нажат пробел, закрываю окно вывода текста


    def start(self):
        '''начинает вывод текста в рамку'''
        x=(self.window.window.winfo_width()//2)-(self.windowbox_img.width()//2)+tk.PhotoImage(file='img/font/space.png').width()*3
        y=(self.window.window.winfo_height()//2)-(self.windowbox_img.height()//2)+(tk.PhotoImage(file='img/font/space.png').height()*1.5)+tk.PhotoImage(file='img/font/space.png').height()
        max_in_line=self.windowbox_img.width()//tk.PhotoImage(file='img/font/space.png').width()
        max_lines=self.windowbox_img.height()//tk.PhotoImage(file='img/font/space.png').height()-2

        self.thread = threading.Thread(target=self.printer.print, args=(self.text, x, y, max_in_line, max_lines, True, self.canvas)) #запускаю в потоке вывод текста о разработчиках
        self.thread.daemon = True
        self.thread.start()
        
        self.bind_keys() #бинд кнопок

    

    def stop(self, *args):
        '''стирает выведенный текст вместе с рамкой'''
        self.window.window.unbind('<KeyPress>')
        self.printer.clear()
        self.canvas.delete('developers_windowbox')
