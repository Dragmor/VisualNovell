'''конструктор игровых сцен'''
from tkinter import *
import tkinter as tk
import threading
import time

from scripts.GUI.printer import *
from scripts.game_engine.main_menu import *
from scripts.game_engine.effects import *
from scripts.game_engine.db import *

'''класс извлекает данные из файла сценария, и собирает на его основе игровые 
сцены'''

class ActConstructor():
    def __init__(self, window):
        self.window = window
        self.height = self.window.height
        self.width = self.window.width
        self.frame = tk.Frame(self.window.window)
        self.effect = Effects() #объект накладывает визуальные эффекты на canvas
        self.main_menu = MainMenu(self.window)
        self.canvas = Canvas(self.frame, bg="white", highlightthickness=0, takefocus=1, width=self.width,  height=self.height) 
        self.canvas.pack()


    def new_game(self, *args):
        '''при нажатии 'новая игра' запускается этот метод, который вытягивает
        данные из файла new_game.s'''
        self.analyse_data(1) #передаёт анализатору данных id первой сцены


    def check_saved_games(self):
        '''метод проверяет, есть ли сохранения, что бы при нажатии на НОВАЯ ИГРА
        показывалось предупреждение, что сохранение будет утеряно. Так же 
        используется для обработки нажатия на ПРОДОЛЖИТЬ'''

        #тут нужно реализовать проверку файла 'saves/save'
        pass


    def load_game(self, *args):
        '''вызывается, если была нажата кнопка 'продолжить'. Пытается открыть
        сохраненную игру. Если сохранения не найдены, вызывает 
        метод new_game'''
        try:
            file=open('saves/save', 'r')
        except:
            self.new_game() #запускаю новую игру, если не удалось открыть сохранку
        '''тут будет проверка, на каком моменте остановился игрок, и будет
        запущен act_generator с нужными параметрами'''

    def analyse_data(self, scene_id):
        '''метод получает данные, извлеченные из файла сценария, и вызывает
        нужный для построения сцены метод'''
        self.db = ScenarioDB() #СУБД
        scene_type, data = self.db.get_scene(scene_id)
        
        if scene_type == 'dialogs':
            self.dialogue(data)
        elif scene_type == 'choose':
            self.choose(data)
        elif scene_type == 'view':
            self.scene_view(data)
        elif scene_type == 'exit': #выход в меню
            self.canvas.bind('<ButtonPress>', self.exit_to_menu)
            self.exit_to_menu()

            

#БЛОК РЕАЛИЗАЦИИ СЦЕНЫ ДИАЛОГА        

    def dialogue(self, data):
        '''сцена диалога
        Порядок следования данных:
        0 - id сцены
        1 - фоновая музыка
        2 - фон сцены
        3 - говорящий персонаж (спрайт)
        4 - имя говорящего
        5 - текст, что он говорит
        6 - накладываемый визуальный эффект
        7 - id следующей сцены
        '''
        
        self.printer = Printer(self.window.window)
        self.next_scene_id = data[-1] #id следующей сцены
        current_id = data[0] #id текущей сцены
        if data[1] != None: #music
            self.window.audio.play('sounds/game/'+data[1], loop=True)
        if data[2] != None: #background
            self.background = tk.PhotoImage(file='img/backgrounds/'+data[2]+'.png')
            self.canvas.create_image(self.width//2, self.height//2, image=self.background, tag='background') #отображаю картинку заднего фона

        #накладываю визуальные эффекты на фон, не на персонажей
        if data[6] == 'blood': #effects
            self.effect.blood_filter(self.canvas)
        elif data[6] == 'gradient':
            self.effect.centre_gradient(self.canvas)
        elif data[6] == 'darkness':
            self.effect.darkness(self.canvas)

        if data[3] != None: #character img

        #позволяет отображать до 4-х персонажей на экране одновременно

            characters = data[3].split('|')
            len_x = self.width//(len(characters)+1)
            x = 0
            for i in range(0, len(characters)):
                x += len_x
                exec('self.character_'+str(i)+' = tk.PhotoImage(file="img/characters/"+characters[i]+".png")')
                exec('self.canvas.create_image(x, self.height//2, image=self.character_'+str(i)+', tag="character_'+str(i)+'")')
        if data[4] != None and data[5] != None: #character name + text
            self.text = data[4].upper()+' \\ '+data[5] #если передан и говорящий, и текст
        elif data[4] == None and data[5] != None: #если не указан говорящий, но есть текст, просто вывожу его
            self.text = data[5]
        else: #если не передан ни текст, ни говорящий, вывожу троеточие
            self.text = '...'

        self.frame.place(x=0, y=0)
        self.frame.focus() #устанавливаю фокус на фрейме
        self.canvas.bind('<ButtonPress>', self.backrolling_or_next) #клик мыши
        self.frame.bind('<KeyPress>', self.dialogue_check_key) #проверка нажатой кнопки

        self.printer.draw_windowbox(canvas=self.canvas)
        thread = threading.Thread(target=self.printer.print, args=(self.text, 0,0,0,0,False,self.canvas))
        thread.daemon = True
        thread.start()
        #накладываю визуальные эффекты, если указаны




    
    def backrolling_or_next(self, *args):
        '''нужно для промотки и пропуска текста в диалоге'''
        if self.printer.backrolling() == False:
            try:
                self.printer.waiting = False
            except:
                pass
        else:
            self.printer.waiting = False

        if self.printer.ended == True: #если выведен весь текст, запускаю 
            #обработку следующей сцены
            self.printer.clear() #очищаю текст
            self.printer.delete_windowbox() #удаляю рамку

            #удаляю бинды, что бы можно было на ентер забиндить другие функции
            self.canvas.unbind('<ButtonPress>')
            self.frame.unbind('<KeyPress>')
            
            self.analyse_data(self.next_scene_id) #переход к следующей сцене

    def dialogue_check_key(self, key):
        '''обработка нажатой клавиши в диалоге'''
        #проверяю нажатую кнопку
        if key.keycode == 13: #кнопка return
            self.backrolling_or_next()
        elif key.keycode == 32: #пробел
            self.backrolling_or_next()
        elif key.keycode == 27: #ESC
            self.exit_to_menu()



#БЛОК РЕАЛИЗАЦИИ СЦЕНЫ ВЫБОРА ДЕЙСТВИЙ

    def choose(self, data):
        '''сцена выбора действия/ответа
        МАКСИМУМ 4 ВАРИАНТА ВЫБОРА
        Порядок следования данных:
        0 - id сцены
        1 - варианты
        2 - id вариантов
        '''
        current_id = data[0] #id текущей сцены
        nums_of_variants = len(data[1].split('|')) #сколько вариантов выбора
        self.select_windowbox_unfocus = tk.PhotoImage(file='img/game/select_windowbox_unfocus.png')
        self.select_windowbox_focus = tk.PhotoImage(file='img/game/select_windowbox_focus.png')
        self.windowbox = tk.PhotoImage(file='img/game/windowbox.png')

        self.canvas.create_image(self.width//2, self.height//2, image=self.windowbox, tag='windowbox') #отображаю рамку

        '''отображение кнопок выбора в отдельных фреймах'''
        for i in range(1, nums_of_variants+1): #создаю кнопки выбора
            y = (self.height//2-self.windowbox.height()//2+((self.windowbox.height()//nums_of_variants)*i)-(self.windowbox.height()//nums_of_variants)//2)-self.select_windowbox_unfocus.height()//2
            max_in_lines = self.select_windowbox_unfocus.width()//tk.PhotoImage(file='img/font/space.png').width()
            exec('self.frame_'+str(i)+' = tk.Frame(self.canvas)') #создаю фрейм кнопки
            exec('self.canvas_'+str(i)+' = Canvas(self.frame_'+str(i)+', bg="white", highlightthickness=0, takefocus=1, width=self.select_windowbox_unfocus.width(),  height=self.select_windowbox_unfocus.height()) ')
            exec('self.canvas_'+str(i)+'.pack()')
            exec('self.canvas_'+str(i)+'.create_image(self.select_windowbox_unfocus.width()//2, self.select_windowbox_unfocus.height()//2, image=self.select_windowbox_unfocus, tag="variant_'+str(i)+'")')
            exec('self.frame_'+str(i)+'.place(x=self.width//2-self.select_windowbox_unfocus.width()//2, y=y)') #размещаю кнопку

            exec('printer=Printer(self.window.window)')
            exec('thread = threading.Thread(target=printer.print, args=(data[1].split("|")[i-1], 0, self.select_windowbox_unfocus.height()//2,max_in_lines,1,True,self.canvas_'+str(i)+', True))')
            exec('thread.daemon = True')
            exec('thread.start()')
            exec('self.var_'+str(i)+'_id = data[2].split("|")[i-1]')
            exec('self.frame_'+str(i)+'.focus()')
            exec('self.frame_'+str(i)+'.bind("<Enter>", self.variant_'+str(i)+'_focus)')
            exec('self.frame_'+str(i)+'.bind("<Leave>", self.variant_'+str(i)+'_unfocus)')
            exec('self.canvas_'+str(i)+'.bind("<ButtonPress>", self.variant_'+str(i)+'_click)')

        exec('del printer')

    def variant_1_focus(self, *args):
        '''навожу мушкой на первый вариант - меняю бэк'''
        self.canvas_1.itemconfigure('variant_1',image=self.select_windowbox_focus)
    def variant_2_focus(self, *args):
        self.canvas_2.itemconfigure('variant_2',image=self.select_windowbox_focus)
    def variant_3_focus(self, *args):
        self.canvas_3.itemconfigure('variant_3',image=self.select_windowbox_focus)
    def variant_4_focus(self, *args):
        self.canvas_4.itemconfigure('variant_4',image=self.select_windowbox_focus)

    def variant_1_unfocus(self, *args):
        '''снимаю курсор с первого варианта'''
        self.canvas_1.itemconfigure('variant_1',image=self.select_windowbox_unfocus)
    def variant_2_unfocus(self, *args):
        self.canvas_2.itemconfigure('variant_2',image=self.select_windowbox_unfocus)
    def variant_3_unfocus(self, *args):
        self.canvas_3.itemconfigure('variant_3',image=self.select_windowbox_unfocus)
    def variant_4_unfocus(self, *args):
        self.canvas_4.itemconfigure('variant_4',image=self.select_windowbox_unfocus)

    def variant_1_click(self, *args):
        self.choose_processing('1')
    def variant_2_click(self, *args):
        self.choose_processing('2')
    def variant_3_click(self, *args):
        self.choose_processing('3')
    def variant_4_click(self, *args):
        self.choose_processing('4')


    def choose_processing(self, choosen_var):
        '''переход к сцене, основанной на выбранном варианте'''
        try:
            self.canvas.delete('windowbox')
            self.frame_1.destroy()
            self.frame_2.destroy()
            self.frame_3.destroy()
            self.frame_4.destroy()
        except:
            pass
        finally:
            exec('self.analyse_data(str(self.var_'+choosen_var+'_id))')



#БЛОК РЕАЛИЗАЦИИ ПОКАЗА СЦЕНЫ БЕЗ ДРУГИХ ЭЛЕМЕНТОВ
    def scene_view(self, data):
        '''
        ПОРЯДОК СЛЕДОВАНИЯ ДАННЫХ:
        0 - id текущей сцены
        1 - музыка текущей сцены
        2 - фон сцены
        3 - персонажы на фоне
        4 - визуальные эффекты
        5 - id следующей сцены
        '''
        current_id = data[0] #id текущей сцены
        self.next_scene_id = data[-1] #id следующей сцены

        if data[1] != None: #audio
            self.window.audio.play('sounds/game/'+data[1], loop=True)
        if data[2] != None: #background
            self.background = tk.PhotoImage(file='img/backgrounds/'+data[2]+'.png') #фон сцены
            self.canvas.create_image(self.width//2, self.height//2, image=self.background, tag='background') #отображаю картинку заднего фона

        #накладываю визуальные эффекты на фон, не на персонажей
        if data[4] == 'blood': #effects
            self.effect.blood_filter(self.canvas)
        elif data[4] == 'gradient':
            self.effect.centre_gradient(self.canvas)
        elif data[4] == 'darkness':
            self.effect.darkness(self.canvas)

        if data[3] != None: #character img

        #позволяет отображать до 4-х персонажей на экране одновременно
            characters = data[3].split('|')
            len_x = self.width//(len(characters)+1)
            x = 0
            for i in range(0, len(characters)):
                x += len_x
                exec('self.character_'+str(i)+' = tk.PhotoImage(file="img/characters/"+characters[i]+".png")')
                exec('self.canvas.create_image(x, self.height//2, image=self.character_'+str(i)+', tag="character_'+str(i)+'")')

        self.frame.focus() #устанавливаю фокус на фрейме
        self.canvas.bind('<ButtonPress>', self.scene_view_goto_next_scene) #клик мыши
        self.frame.bind('<KeyPress>', self.scene_view_check_key) #проверка нажатой кнопки


    def scene_view_check_key(self, key):
        '''обработка нажатой клавиши'''
        #проверяю нажатую кнопку
        if key.keycode == 13: #кнопка return
            self.scene_view_goto_next_scene() #переход к следующей сцене
        elif key.keycode == 32: #пробел
            self.scene_view_goto_next_scene() #переход к следующей сцене
        elif key.keycode == 27: #ESC
            self.exit_to_menu()

    def scene_view_goto_next_scene(self, *args):
        '''переходит к следующей сцене'''
        self.analyse_data(self.next_scene_id)


#-----------------------------------------------------------------------------#
    def exit_to_menu(self, *args):
        '''отрисовывка менюшки
        поверх фрейма игры'''
        self.main_menu.draw()
        self.main_menu.bind()
        thread = threading.Thread(target=self.pause)
        thread.daemon = True
        thread.start()

    def pause(self, *args):
        '''пауза, запускаемая в потоке. Нужна для установки
        фокуса на фрейме, что бы работали бинды'''
        while self.main_menu.pause:
            if self.main_menu.pause == 'new_game':
                break
            time.sleep(0.1)
        self.frame.focus()
        self.frame.bind('<Key-Escape>', self.exit_to_menu)
        if self.main_menu.pause == 'new_game':
            self.main_menu.pause = False
            self.new_game()
