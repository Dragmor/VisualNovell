from tkinter import *
import tkinter as tk
import threading
import time
import sqlite3

'''
ПРОБУЮ СОЗДАТЬ JRPG ДВИЖОК С ВИДОМ СВЕРХУ

-Нужно создать стандартный набор спрайтов персонажа, хранящиеся в массиве images
Хранить в определенной последовательности, что бы оперировать спрайтами по их
индексу.
-Сделать проверку столкновений, и проверку под ногами
'''
class BaseChar():
    '''базовый класс бойца'''
    def __init__(self, window=None, canvas=None, name='default', x=0, y=0, speed=0, health=100):
        self.canvas = canvas
        self.x = x #координаты местоположения
        self.y = y
        self.speed = speed
        self.health = health
        self.images = [] #спрайты персонажа
        self.name = name
        self.images.append(tk.PhotoImage(file='hero.png')) #спрайт лицом вперед


        # self.images.append(tk.PhotoImage(file='temp_develope/hero_left.png')) #лицом влево
        # self.images.append(tk.PhotoImage(file='temp_develope/hero_right.png')) #лицом вправо


        self.canvas.create_image(self.x, self.y, image=self.images[0], tag=name) #отображаю в canvas
        self.window = window
        self.jumping_height = 200 #высота, на которую может подпрыгнуть перс
        self.is_jump = False #флаг, в прыжке ли перс
        self.is_staying = True #флаг, стоит ли перс на чём то


    def get_x(self):
        return self.canvas.coords(self.name)[0] #возвращает координаты x перса
    def get_y(self):
        return self.canvas.coords(self.name)[1]
    def get_speed(self):
        return(self.speed) 
    def get_health(self): #возвращает кол-во хп
        return self.health
    def garner_damage(self, damage): #получает урон
        self.health -= damage
    def move_to(self, x=0, y=0): #перемещаю по абсолютным координатам
        self.canvas.move(self.name, -self.canvas.coords(self.name)[0]+x, -self.canvas.coords(self.name)[1]+y)
    def move(self, x=0, y=0, *args): #перемещаю относительно текущей позиции
        #проверка, не выходит ли перс за границы экрана
        if self.canvas.coords(self.name)[0]+x > 1024:
            return
        elif self.canvas.coords(self.name)[0]+x < 0:
            return

        self.canvas.move(self.name, x, y)


class MainHero(BaseChar):
    def __init__(self, window=None, canvas=None, name='default', x=0, y=0, speed=0, health=100):
        '''
        родительское окно
        холст
        имя персонажа
        координаты
        скорость передвижения
        здоровье
        '''
        BaseChar.__init__(self, window, canvas, name, x, y, speed, health) #вызов конструктора базового класса
        self.pressed_keys = [] #список нажатых клавиш
        #запускаю обработчик нажатых клавиш в потоке
        self.key_thread = threading.Thread(target=self.key_processing)
        self.key_thread.daemon = True
        self.key_thread.start()
        #запускаю обработчик анимации персонажа в потоке
        self.animation_thread=threading.Thread(target=self.animations)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        #
        self.window.bind('<KeyPress>' , self.key_press)
        self.window.bind('<KeyRelease>' , self.key_release)
        #


    def animations(self):
        '''метод отвечает за анимацию при движении персонажа.
        Метод должен работать в вечном цикле в отдельном потоке.
        Скорость анимации передавать в параметрах, и использовать в sleep'''
        self.move_down = [tk.PhotoImage(file='hero_down_1.png'), tk.PhotoImage(file='hero_down_2.png'), tk.PhotoImage(file='hero_down_3.png')]
        self.move_up = [tk.PhotoImage(file='hero_up_1.png'), tk.PhotoImage(file='hero_up_2.png'), tk.PhotoImage(file='hero_up_3.png')]
        self.move_right = [tk.PhotoImage(file='hero_right_1.png'), tk.PhotoImage(file='hero_right_2.png'), tk.PhotoImage(file='hero_right_3.png')]
        while True:
            i=0
            while 40 in self.pressed_keys: #если перс идёт вниз
                if i >= len(self.move_down):
                    i = 0
                canvas.itemconfigure('hero',image=self.move_down[i])
                i+=1
                time.sleep(0.1)

            while 38 in self.pressed_keys: #если перс идёт вверх
                if i >= len(self.move_up):
                    i = 0
                canvas.itemconfigure('hero',image=self.move_up[i])
                i+=1
                time.sleep(0.1)

            while 39 in self.pressed_keys: #если перс идёт вправо
                if i >= len(self.move_up):
                    i = 0
                canvas.itemconfigure('hero',image=self.move_right[i])
                i+=1
                time.sleep(0.1)

    def key_press(self, key):
        if key.keycode not in self.pressed_keys: #если кнопка нажата, но ещё не добавлена в список:
            self.pressed_keys.append(key.keycode) #добавляю кнопку в список нажатых
        
    def key_release(self, key): #если кнопка отпущена, удаляю её кейкод из списка кнопок
        self.pressed_keys.remove(key.keycode)

    def key_processing(self): #вывожу список, какие кнопки нажаты сейчас
        while True:
            if 40 in self.pressed_keys: #вниз
                self.move(0, self.speed)
            elif 38 in self.pressed_keys: #вверх
                self.move(0, -self.speed)
            if 39 in self.pressed_keys: #вправо
                self.move(self.speed, 0)
            elif 37 in self.pressed_keys: #влево
                self.move(-self.speed, 0)
            # else: #если не нажата ни одна из кнопок влево-вправо
                # canvas.itemconfigure(self.name, image=self.images[0])

            time.sleep(0.01)













window = tk.Tk()


canvas = Canvas(window, bg="white", highlightthickness=0, takefocus=1, width=1024,  height=768)
# canvas.create_image(512, 379, t)
canvas.pack() 



hero = MainHero(window=window, canvas=canvas, name='hero' ,x=100, y=100, speed=5)

window.mainloop()

