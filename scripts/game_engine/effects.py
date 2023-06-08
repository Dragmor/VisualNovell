from tkinter import *
import tkinter as tk

class Effects():
    '''Класс реализует визуальные эффекты (фильтры), накладываемые на уже
    отрисованную сцену
    '''
    def __init__(self):
        pass

    def blood_filter(self, canvas):
        '''накладывает на фрейм эффект крови
        Что бы отобразить эффект: self.effect.blood_filter(self.canvas)'''
        self.effect = tk.PhotoImage(file='img/effects/blood.png')
        canvas.create_image(self.effect.width()//2, self.effect.height()//2, image=self.effect, tag='effect')

    def centre_gradient(self, canvas):
        '''накладывает на фрейм эффект градиента'''
        self.effect = tk.PhotoImage(file='img/effects/centre_gradient.png')
        canvas.create_image(self.effect.width()//2, self.effect.height()//2, image=self.effect, tag='effect')

    def darkness(self, canvas):
        '''накладывает на фрейм эффект затемнения фона'''
        self.effect = tk.PhotoImage(file='img/effects/darkness.png')
        canvas.create_image(self.effect.width()//2, self.effect.height()//2, image=self.effect, tag='effect')

    def rain(self, canvas):
        '''эффект идущего дождя (с анимацией)'''
        pass
        