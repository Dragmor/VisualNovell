from tkinter import *
import tkinter as tk
import time

from scripts.settings_parser import *

class Printer():
    '''Класс реализует вывод на экран текста сторонними шрифтами в картинках.
    Выводит со скоросью text_speed (от 1 до 100)
    в координатах x и y
    
        МЕТОДЫ КЛАССА
    self.window.printer.print(text='текст') #выведет текст
    self.window.printer.clear() #очистит вывод текста
    self.window.printer.draw_windowbox() #отрисует рамку для текста
    self.window.printer.delete_windowbox()

        ПОМОЩЬ
    #'\': #символ, используется для перехода на новую строку! Если нужен переход на несколько строк, а не на одну, то писать нужно не подряд (\\\\) а через пробел (\ \ \ \)
    #'^' #используется, если нужно вывести подряд несколько пробелов (т.к. просто несколько пробелов не сработает, ибо использована функция .split() при парсе)
    '''





    '''
    ОСТАВИТЬ ОДИН ФРЕЙМ, ФРЕЙМЫ СТРОК ЗАМЕНИТЬ КАНВАСАМИ, ЛЕЙБЛЫ БУКВ ЗАМЕНИТЬ
    КАНВАС.КРИЕЙТ_ИМЕЙДЖ! ТОГДА ФОН РАМКИ МОЖЕТ БЫТЬ НЕ БЕЛЫЙ, НО КРАЯ
    РАМКИ ВСЁ РАВНО БУДУТ НЕПРОЗРАЧНЫ (Т.К. РАМКА НАХОДИТСЯ НА ФРЕЙМЕ!) можно
    конечно попробовать в аргументах передать канвас, на котором будет выводиться
    текст и рамка, но скорее всего это слишком геморрно
    '''
    def __init__(self, window, text_speed=None):
        '''если в параметрах не передается значение text_speed, то он берет
        эти значения из settings.ini'''
        self.window = window
        self.ended = True #True - весь текст выведен, False - ещё выводится
        self.settings = SettingsParser()
        if text_speed == None:
            self.text_speed = (2/int(self.settings.get_option_value('text_speed')))/2 #скорость вывода текста
            self.temp_text_speed = self.text_speed #переменная, для изменения скорости текста
        else:
            self.text_speed = (2/text_speed)/2 #скорость вывода текста
            self.temp_text_speed = self.text_speed #переменная, для изменения скорости текста
        self.text_lines = [] #список, содержащий фреймы, куда будет выводиться текст
        self.font_array = [] #массив шрифта
        self.chars_array = [] #массив символов
        self.windowbox_img = tk.PhotoImage(file='img/game/text_windowbox.png') #изображение рамки для текста

    def __del__(self):
        try:
            self.clear()
        except:
            pass


    def print(self, text='', x=0, y=0, max_in_line=0, max_lines=0, centre=False, canvas=None, choose=False):
        '''метод выводит текст на экран. Если координаты не указаны, выводить
        начинает в координатах, где по дефолту рисуется рамка
        max_in_line - сколько символов может поместиться в одну строку 
        max_lines - сколько строк может поместиться в рамку
        centre - если True, то будет центрировать текст, начиная печатать с середины фрейма (использовано при выводе текста в меню 'РАЗРАБОТЧИКИ')
        '''
        self.exit = False #флаг, что нужно прекратить вывод текста
        self.ended = False
        self.canvas = canvas
        self.text_speed = (2/int(self.settings.get_option_value('text_speed')))/2
        self.temp_text_speed = (2/int(self.settings.get_option_value('text_speed')))/2

        if x==0:
            x = ((self.window.winfo_width()//2)-(self.windowbox_img.width()//2)+tk.PhotoImage(file='img/font/space.png').width()*2)
        if y==0:
            y = self.window.winfo_height()-int((self.windowbox_img.height()*1.2))+tk.PhotoImage(file='img/font/space.png').height()+(tk.PhotoImage(file='img/font/space.png').height()//2)

        #рассчитываю, сколько символов может вместиться в строке, и сколько
        #строк вмещается в рамку, если эти значения не переданы в параметрах


                
        if max_in_line==0:
            max_in_line=self.windowbox_img.width()//tk.PhotoImage(file='img/font/space.png').width()-3
        if max_lines==0:
            max_lines=self.windowbox_img.height()//tk.PhotoImage(file='img/font/space.png').height()-2
        
        chars_count = 0 #счётчик, сколько символов уже выведено в строку
        line_count = 0 #счётчик, сколько строк уже выведено

        if choose:
            '''это флаг, который означает, что текст выводится в Выбор Варианта
            в игре'''
            if len(text)%2: #если число чётное
                x = -tk.PhotoImage(file='img/font/space.png').width()//4+((max_in_line-len(text))//2)*tk.PhotoImage(file='img/font/space.png').width()
            else: #если нечётное, сдигаю вправо ещё на ширину полсимвола
                x = -tk.PhotoImage(file='img/font/space.png').width()//4+((max_in_line-len(text))//2)*tk.PhotoImage(file='img/font/space.png').width()+tk.PhotoImage(file='img/font/space.png').width()//2

        elif centre: #если включено центрирование, предварительно обрабатываю выводимый текст, добавляя ^
            output_text = '' #строка, которая будет использоваться для записи в неё обработанного текста
            for line in text.split('\n'):
                output_text+='^'*((max_in_line-len(line))//2-3)
                output_text+=line+'\n'
            text = output_text



        self.words_list = text.split() #список слов, которые нужно вывести
        self.normal_speed() #возвращаю изначальную скорость текста (на случай, если она была изменена методом backrolling)

        for word in self.words_list: #прохожусь по всем словам

            if line_count >= max_lines-1: #если текст выводится в крайнюю строку
                if len(word) >= max_in_line-chars_count-4:  #если слово не вмещается в строку с учётом 3х точек
                    for i in range(1, 4):
                        self.font_array.append(tk.PhotoImage(file='img/font/dot.png'))

                        self.canvas.create_image(x+(i*tk.PhotoImage(file='img/font/space.png').width())+chars_count*tk.PhotoImage(file='img/font/space.png').width(), y+line_count*tk.PhotoImage(file='img/font/space.png').height(), image=self.font_array[-1], tag='letter')

                    chars_count=max_in_line #делаю это, что бы 100% попасть в следующий блок if
            
            if len(word) > max_in_line-chars_count-1: #если слово не вмещается в строку (с учётом пробела в конце)
                line_count+=1 #перевожу строку
                chars_count=0 #обнуляю счётчик символов в строке, т.к. строка новая
                if line_count >= max_lines: #если переполнено кол-во допустимых строк, то
                    line_count=0 #сбрасываю в 0 счётчик строк
                    self.wait_action() #перед тем как стереть текст, жду сигнала от пользователя
                    self.continue_print(max_lines) #вызываю метод, который стирает выведенный текст, и выводит продолжение текста с первой строки.

            #тут проверяется, какой спрайт символа нужно вывести.
            for char in word: #прохожусь по символам слова
                if self.exit: #если установлен флаг, что нужно прекратить вывод текста, возвращаюсь из функции
                    self.canvas.delete('letter') #удаляю выведенные буквы
                    return

                chars_count+=1 #счётчик букв в строке
                if char == '.':
                    self.font_array.append(tk.PhotoImage(file='img/font/dot.png'))
                elif char =='*':
                    self.font_array.append(tk.PhotoImage(file='img/font/asterisk.png'))
                elif char =='^':
                    self.font_array.append(tk.PhotoImage(file='img/font/space.png'))
                elif char =='"':
                    self.font_array.append(tk.PhotoImage(file='img/font/double_backspark.png'))
                elif char =="'":
                    self.font_array.append(tk.PhotoImage(file='img/font/backspark.png'))
                elif char =='&':
                    self.font_array.append(tk.PhotoImage(file='img/font/ampersand.png'))
                elif char ==':':
                    self.font_array.append(tk.PhotoImage(file='img/font/colon.png'))
                elif char == ',':
                    self.font_array.append(tk.PhotoImage(file='img/font/comma.png'))
                elif char == '?':
                    self.font_array.append(tk.PhotoImage(file='img/font/enquiry.png'))
                elif char == '\\': #символ, используемый для переноса строки!
                    chars_count = max_in_line
                    break
                else: #если символ, который нужно вывести - буква, то проверяю её регистр
                    if char.isupper(): #если буква верхнего регистра, то открываю спрайт буквы
                        #верхнего регистра (uc - UpperCase, верхний регистр)
                        self.font_array.append(tk.PhotoImage(file='img/font/%s_uc.png' %char))
                    elif char.islower(): #если же буква строчная, буре соответствующий спрайт
                        self.font_array.append(tk.PhotoImage(file='img/font/%s.png' %char))
                    else: #если выводимый символ не поддерживается шрифтами, вывоже вместо него символ unsupported_char
                        try:
                            self.font_array.append(tk.PhotoImage(file='img/font/%s.png' %char))
                        except:
                            self.font_array.append(tk.PhotoImage(file='img/font/unsupported_char.png'))


                

                self.canvas.create_image(x+chars_count*tk.PhotoImage(file='img/font/space.png').width(), y+line_count*tk.PhotoImage(file='img/font/space.png').height(), image=self.font_array[-1], tag='letter')
                if char =='^' and centre:
                    pass
                else:
                    time.sleep(self.text_speed) #скорость вывода текста

            chars_count+=1 #добавляю в счётчик символ пробела
            self.font_array.append(tk.PhotoImage(file='img/font/space.png')) #вывожу пробел

        self.backrolling()
        self.ended = True
        self.wait_action() #перед тем как стереть текст, жду сигнала от пользователя, что текст был прочитан



    def backrolling(self, *args):
        '''метод ускоряет вывод текста до максимума. Нужен, что бы была возможность
        промотать текст'''
        if self.temp_text_speed == self.text_speed: #если текст ещё не ускорен, ускоряю
            self.temp_text_speed = self.text_speed
            self.text_speed = 0
            return False #если проматка успешно включена, возвращаю False
        else:
            return True
            #возвращает True, если текст уже проматывается

    def normal_speed(self, *args):
        '''метод возвращает нормальную скорость вывода текста. Применять после
        применения backrolling'''
        self.text_speed = self.temp_text_speed

    def continue_print(self, max_lines):
        '''метод вызывается, когда рамка заполненна текстом. Метод очищает
        выведенный ранее текст с экрана, что позволяет продолжать выводить.
        '''
        self.canvas.delete('letter')

        self.text_lines = []

        self.normal_speed() #возвращаю изначальную скорость текста (на случай, если она была изменена методом backrolling)

    def wait_action(self):
        '''тут происходит ожидание сигнала от пользователя, что он прочитал
        текст, что бы можно было его стереть'''
        self.waiting = True
        while self.waiting == True:
            time.sleep(0.1)
            #вечный цикл ожидания

    def clear(self):
        '''очищает выведенный текст, передавая в print флаг, что нужно
        прекратить выводить текст, и очистить выведенные буквы, а так же
        самостоятельно удаляет выведенные буквы, что бы наверняка'''
        self.exit = True #флаг, что нужно прекратить вывод текста
        self.canvas.delete('letter') #удаляю рамку


    def draw_windowbox(self, x=0, y=0, canvas=None):
        '''отображает рамку, в которой будет выводиться текст. Если x и y
        не переданы, то выводится будет внизу экрана'''
        self.canvas = canvas

        if x==0:
            x = (self.window.winfo_width()//2)-(self.windowbox_img.width()//2)+self.windowbox_img.width()//2
        if y==0:
            y = self.window.winfo_height()-int((self.windowbox_img.height()*1.2))+self.windowbox_img.height()//2

        self.canvas.create_image(x, y, image=self.windowbox_img, tag='printer_windowbox')


    def delete_windowbox(self):
        '''уничтожает выведенную рамку'''
        self.canvas.delete('printer_windowbox') #удаляю рамку
