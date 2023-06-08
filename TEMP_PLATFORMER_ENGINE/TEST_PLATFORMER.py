from tkinter import *
import tkinter as tk
import threading
import time
import sqlite3

'''
ПРОБУЮ СОЗДАТЬ ФАЙТИНГ ТИПА МК2 (Очень гемморно, т.к. нужно делать море
анимаций, проверку на прикосновения, много событий, и т.д.)

-Нужно создать стандартный набор спрайтов персонажа, хранящиеся в массиве images
Хранить в определенной последовательности, что бы оперировать спрайтами по их
индексу.
-Сделать проверку столкновений, и проверку под ногами
-Попробовать сделать руки-ноги отдельными объектами
-заменить time.sleep() на переменную времени
-придумать алгоритм синхронизации игрового времени
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
        self.images.append(tk.PhotoImage(file='temp_develope/hero_down.png')) #спрайт лицом вперед


        self.images.append(tk.PhotoImage(file='temp_develope/hero_left.png')) #лицом влево
        self.images.append(tk.PhotoImage(file='temp_develope/hero_right.png')) #лицом вправо


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

    def jump(self): #перс прыгает
        self.jump_thread=threading.Thread(target=self.jumping)
        self.jump_thread.daemon = True
        self.jump_thread.start()

    def jumping(self):
        '''потоковый метод обработки прыжка'''
        if self.is_jump == False:
            self.is_jump = True
            self.is_staying = False
            for i in range(0, self.jumping_height, self.speed):
                self.move(0, -self.speed*2)
                # self.move_to(x=self.get_x(), y=self.get_y()-self.speed*2)
                time.sleep(0.01)
            self.falling() #запускаю падение
            self.is_jump = False

    def falling(self):
        '''метод падения персонажа (гравитация)'''
        while (not self.is_staying):
            self.move(0, self.speed*2)
            time.sleep(0.01)
            if self.canvas.coords(self.name)[1] > 700:
                self.is_staying = True

    def is_staying(self):
        '''возвращает true, если перс стоит на чём то'''
        pass


    # def draw(self):
        '''отрисовывает спрайт перса в x/y'''
        # self.canvas.create_image(x=10, y=10, image=None, tag='1') #отображаю в canvas

class MainHero(BaseChar):
    def __init__(self, window=None, canvas=None, name='default', x=0, y=0, speed=0, health=100):
        BaseChar.__init__(self, window, canvas, name, x, y, speed, health) #вызов конструктора базового класса
        self.pressed_keys = [] #список нажатых клавиш
        #запускаю обработчик нажатых клавиш в потоке
        self.key_thread = threading.Thread(target=self.key_processing)
        self.key_thread.daemon = True
        self.key_thread.start()
        #
        self.window.bind('<KeyPress>' , self.key_press)
        self.window.bind('<KeyRelease>' , self.key_release)
        #



    def key_press(self, key):
        if key.keycode not in self.pressed_keys: #если кнопка нажата, но ещё не добавлена в список:
            self.pressed_keys.append(key.keycode) #добавляю кнопку в список нажатых
        
    def key_release(self, key): #если кнопка отпущена, удаляю её кейкод из списка кнопок
        self.pressed_keys.remove(key.keycode)

    def key_processing(self): #вывожу список, какие кнопки нажаты сейчас
        while True:
            if 40 in self.pressed_keys: #вниз
                self.canvas.move(self.name, 0, self.speed)
                # canvas.itemconfigure(self.name, image=images[1])
            elif 38 in self.pressed_keys: #вверх
                self.jump()
                # self.canvas.move(self.name, 0, -self.speed)
                # canvas.itemconfigure('hero',image=hero_up)
            if 39 in self.pressed_keys:
                self.move(self.speed, 0)
                canvas.itemconfigure(self.name, image=self.images[2])
            elif 37 in self.pressed_keys:
                canvas.itemconfigure(self.name, image=self.images[1])
                self.move(-self.speed, 0)
            else: #если не нажата ни одна из кнопок влево-вправо
                canvas.itemconfigure(self.name, image=self.images[0])

            time.sleep(0.01)













window = tk.Tk()


canvas = Canvas(window, bg="white", highlightthickness=0, takefocus=1, width=1024,  height=768)
# canvas.create_image(512, 379, t)
canvas.pack() 



hero = MainHero(window=window, canvas=canvas, name='hero' ,x=100, y=700, speed=5)

window.mainloop()

