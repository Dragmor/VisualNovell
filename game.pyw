from scripts.GUI.main_menu import *
from scripts.GUI.window import *
from scripts.GUI.logo import *
from scripts.options import *


import threading

if __name__ == "__main__":
    options = Options()
    window = GUI(screen_resolution='1024x768', text_speed=options.text_speed, animation_speed=options.animation_speed, options=options) #создаю окно
    main_menu = MainMenu(window)

    #блок запуска заставки игры
    logo = Logo(window, main_menu) #создаю объект заставки
    process = threading.Thread(target=logo.start) #запускаю заставку в 
    process.daemon = True                         #отдельном потоке
    process.start()
    #конец блока заставки
    del logo
    

    window.loop() #зацикливаю окно
