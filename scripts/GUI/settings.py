'''класс фрейма настроек игры'''
from tkinter import *
import tkinter as tk
import time
import threading

import scripts.GUI.main_menu


class Settings():
    '''тут объявлен класс для пункта меню НАСТРОЙКИ. Манипуляции с объектом
    этого класса происходят в файле mainmenu.py'''

    def __init__(self, window, main_frame):
        self.window = window
        self.main_frame = main_frame
        self.frame = tk.Frame(self.main_frame)
        self.text_speed = self.window.options.text_speed
        self.animation_speed = self.window.animation_speed


        self.width = window.width # получаем ширину экрана
        self.height = window.height # получаем высоту экрана

        #вывожу задний фон
        self.background = tk.PhotoImage(file='img/settings/settings_background.png')
        self.back_unfocus = tk.PhotoImage(file='img/buttons/back_unfocus.png')
        self.back_focus = tk.PhotoImage(file='img/buttons/back_focus.png')
        self.settings_windowbox = tk.PhotoImage(file='img/settings/settings_windowbox.png')
        self.ts_adjustable_line_image = tk.PhotoImage(file='img/settings/ts_adjustable_line.png')
        self.as_adjustable_line_image = tk.PhotoImage(file='img/settings/as_adjustable_line.png')
        self.as_slat_image = tk.PhotoImage(file='img/settings/slat.png')
        self.sound_on = tk.PhotoImage(file='img/settings/sounds_on.png')
        self.sound_off = tk.PhotoImage(file='img/settings/sounds_off.png')
        self.ts_slat_image = tk.PhotoImage(file='img/settings/slat.png')


        self.canvas = Canvas(self.frame, bg="white", highlightthickness=0, takefocus=1, width=self.width,  height=self.height)
        self.canvas.create_image(self.background.width()//2, self.background.height()//2, image=self.background, tag='background') #отображаю фон
        self.canvas.create_image(self.width-self.back_unfocus.width()//2, self.height-self.back_unfocus.height()*2, image=self.back_unfocus, tag='back')
        self.canvas.create_image(self.width//2, self.height//2, image=self.settings_windowbox, tag='windowbox') #рамка для настроек

        #отрисовываю ползунки скоростей
        self.text_speed_regulator() #отображаю ползунки регулировок скорости
        self.sounds_button()
        self.animation_speed_regulator() #отображаю ползунки регулировок скорости

        self.canvas.pack()

        #бинд кнопок
        self.bind()
            

    def bind(self, *args):
        #непосредственно бинд
        self.canvas.tag_bind('back','<Enter>', self.back_white_sprite)
        self.canvas.tag_bind('back','<Leave>', self.back_unfocuslack_sprite)
        self.canvas.tag_bind('back','<ButtonPress>', self.back_processing)
        #бинды ползунков скоростей
        self.canvas.tag_bind('ts_adjustable_line','<ButtonPress>', self.move_ts_slat)
        self.canvas.tag_bind('as_adjustable_line','<ButtonPress>', self.move_as_slat)

        self.canvas.tag_bind('ts_slat','<ButtonPress>', self.click_ts_slat)
        self.canvas.tag_bind('as_slat','<ButtonPress>', self.click_as_slat)

        #бинд кнопки отключения звуков
        self.canvas.tag_bind('mute','<ButtonPress>', self.click_on_mute_button)


    def back_processing(self, *args):
        '''метод запускает в потоке переход в гл. меню из настроек'''
        process = threading.Thread(target=self.start)
        process.daemon = True
        process.start()

    def start(self):
        #непосредственно поток
        for i in range(self.height, 0, -self.window.options.animation_speed):
            self.draw(x=0, y=-i)
            time.sleep(0.01) #задержка обновления кадров
        self.draw(x=0, y=0)

    def text_speed_regulator(self):
        '''метод выводит ползунок регулировки скорости вывода текста'''
        #вывожу рамку для регулятора скорости текста
        
        self.ts_max_x = self.width//2+self.ts_adjustable_line_image.width()//2-self.ts_slat_image.width()//2 #границы, за которые не должен выходить ползунок
        self.ts_min_x = self.width//2-self.ts_adjustable_line_image.width()//2+self.ts_slat_image.width()//2 #границы, за которые не должен выходить ползунок

        self.ts_section = self.ts_adjustable_line_image.width()//100 #секция = 1/100 ширины полосы, что бы можно было выставлять ползунок по значению
        self.ts_value = self.window.options.text_speed*100//500 #значение скорости, по которому устанавливается ползунок

        adjustable_line_x = self.width//2-self.ts_adjustable_line_image.width()//2+self.ts_adjustable_line_image.width()//2 #где вывожу регулятор
        adjustable_line_y = self.height//2-self.settings_windowbox.height()//2 + self.ts_adjustable_line_image.height() +self.ts_adjustable_line_image.height()//2

        self.canvas.create_image(adjustable_line_x, adjustable_line_y, image=self.ts_adjustable_line_image, tag='ts_adjustable_line')
        
        #проверяю, куда установить ползунок
        if self.window.options.text_speed > 490:
            self.canvas.create_image(self.ts_max_x, adjustable_line_y, image=self.ts_slat_image, tag='ts_slat')
        elif self.window.options.text_speed < 10:
            self.canvas.create_image(self.ts_min_x, adjustable_line_y, image=self.ts_slat_image, tag='ts_slat')
        else:
            self.canvas.create_image(self.ts_min_x+self.ts_value*self.ts_section, adjustable_line_y, image=self.ts_slat_image, tag='ts_slat')



    def move_ts_slat(self, arg):
        '''двигает ползунок'''
        #проверка, не выходит ли ползунок за пределы
        x = self.canvas.coords('ts_slat')[0]
        #если выходит за пределы вправо
        if x+arg.x-x > self.width//2+self.ts_adjustable_line_image.width()//2-self.ts_slat_image.width()//2:
            self.canvas.move('ts_slat', self.width//2+self.ts_adjustable_line_image.width()//2-self.ts_slat_image.width()//2-x, 0)
        #если уходит влево
        elif x+arg.x-x < self.width//2-self.ts_adjustable_line_image.width()//2+self.ts_slat_image.width()//2:
            self.canvas.move('ts_slat', self.width//2-self.ts_adjustable_line_image.width()//2+self.ts_slat_image.width()//2-x, 0)

        else:
            self.canvas.move('ts_slat', arg.x-x, 0)

        x = self.canvas.coords('ts_slat')[0]
        self.ts_new_value = (x-self.ts_min_x)//self.ts_section
        self.window.options.change_option('text_speed', str(int(self.ts_new_value*(500/(self.ts_adjustable_line_image.width()//self.ts_section))+5))) #записываю новое значение в settings.ini

    def click_ts_slat(self, arg):
        '''при нажатии на ползунок, перемещает его на максимум либо на минимум,
        в зависимости от его текущего положения'''
        if self.window.options.text_speed < 250:
            var=510
            self.canvas.move('ts_slat', -self.canvas.coords('ts_slat')[0]+self.ts_max_x, 0)
        elif self.window.options.text_speed > 250:
            var=0
            self.canvas.move('ts_slat', -self.canvas.coords('ts_slat')[0]+self.ts_min_x, 0)
        else:
            var=510
            self.canvas.move('ts_slat', -self.canvas.coords('ts_slat')[0]+self.ts_max_x, 0)

        self.window.options.change_option('text_speed', var)


    def animation_speed_regulator(self):
        # pass
        '''метод выводит ползунок регулировки скорости анимации'''
        self.as_max_x = self.background.width()//2+self.as_adjustable_line_image.width()//2-self.as_slat_image.width()//2 #границы, за которые не должен выходить ползунок
        self.as_min_x = self.background.width()//2-self.as_adjustable_line_image.width()//2+self.as_slat_image.width()//2 #границы, за которые не должен выходить ползунок

        self.as_section = self.ts_adjustable_line_image.width()//100 #секция = 1/100 ширины полосы, что бы можно было выставлять ползунок по значению
        self.as_value = self.window.options.animation_speed*100//50 #значение скорости, по которому устанавливается ползунок

        adjustable_line_x = self.width//2-self.as_adjustable_line_image.width()//2+self.as_adjustable_line_image.width()//2 #где вывожу регулятор
        adjustable_line_y = self.height//2+self.settings_windowbox.height()//2 - self.as_adjustable_line_image.height() - self.as_adjustable_line_image.height()//2

        self.canvas.create_image(adjustable_line_x, adjustable_line_y, image=self.as_adjustable_line_image, tag='as_adjustable_line')

        #проверяю, куда установить ползунок
        if self.window.options.animation_speed > 45:
            self.canvas.create_image(self.as_max_x, adjustable_line_y, image=self.as_slat_image, tag='as_slat')
        elif self.window.options.animation_speed < 6:
            self.canvas.create_image(self.as_min_x, adjustable_line_y, image=self.as_slat_image, tag='as_slat')
        else:
            self.canvas.create_image(self.as_min_x+self.as_value*self.as_section, adjustable_line_y, image=self.as_slat_image, tag='as_slat')

    def move_as_slat(self, arg):
        '''двигает ползунок'''

        #проверка, не выходит ли ползунок за пределы
        x = self.canvas.coords('as_slat')[0]

        if x+arg.x-x > self.width//2+self.as_adjustable_line_image.width()//2-self.as_slat_image.width()//2:
            self.canvas.move('as_slat', self.width//2+self.as_adjustable_line_image.width()//2-self.as_slat_image.width()//2-x, 0)

        elif x+arg.x-x < self.width//2-self.as_adjustable_line_image.width()//2+self.as_slat_image.width()//2:
            self.canvas.move('as_slat', self.width//2-self.as_adjustable_line_image.width()//2+self.as_slat_image.width()//2-x, 0)

        else:
            self.canvas.move('as_slat', arg.x-x, 0)

        x = self.canvas.coords('as_slat')[0]
        self.as_new_value = (x-self.as_min_x)//self.as_section
        self.window.options.change_option('animation_speed', str(int(self.as_new_value*(50/(self.as_adjustable_line_image.width()//self.as_section))+5))) #записываю новое значение в settings.ini


    def click_as_slat (self, arg):
        '''при нажатии на ползунок, перемещает его на максимум либо на минимум,
        в зависимости от его текущего положения'''
        if self.window.options.animation_speed < 25:
            var=510
            self.canvas.move('as_slat', -self.canvas.coords('as_slat')[0]+self.as_max_x, 0)
        elif self.window.options.animation_speed > 25:
            var=0
            self.canvas.move('as_slat', -self.canvas.coords('as_slat')[0]+self.as_min_x, 0)
        else:
            var=510
            self.canvas.move('as_slat', -self.canvas.coords('as_slat')[0]+self.as_max_x, 0)

        self.window.options.change_option('animation_speed', var)
        

    def sounds_button(self):
        '''создаёт кнопку ВКЛ/ОТКЛ звука'''
        
        sound_button_x = self.width//2-self.as_adjustable_line_image.width()//2+self.sound_on.width()//2 #где вывожу кнопку
        sound_button_y = self.height//2

        if self.window.options.mute == 'false':
            self.canvas.create_image(sound_button_x, sound_button_y, image=self.sound_on, tag='mute')
        else:
            self.canvas.create_image(sound_button_x, sound_button_y, image=self.sound_off, tag='mute')


    
    def click_on_mute_button(self, *args):
        '''обработчик нажатий на кнопку вкл-выкл звук'''
        if self.window.options.mute == 'false':
            self.window.options.change_option('mute','true')
            self.canvas.itemconfigure('mute',image=self.sound_off)
            self.window.audio.stop()
        else:
            self.window.options.change_option('mute','false')
            self.canvas.itemconfigure('mute',image=self.sound_on)
            self.window.audio.play('sounds/menu/background', loop=True) #запускаю мелодию менюшки


    def back_white_sprite(self, *args):
        self.canvas.itemconfigure('back',image=self.back_focus)
    def back_unfocuslack_sprite(self, *args):
        self.canvas.itemconfigure('back',image=self.back_unfocus)


    def draw(self, x=0, y=0):
        '''отрисовка фрейма настроек в координатах'''
        self.main_frame.place(x=x, y=y) 
