from scripts.settings_parser import *

class Options():
    '''класс хранит в себе настройки игры, что бы постоянно не парсить
    их из файла'''
    def __init__(self):
        '''получаю из парсера значения настроек'''
        self.settings = SettingsParser()
        self.animation_speed, self.text_speed, self.mute = self.settings.parse() #получаю настройки игры из файла settings.ini

    def change_option(self, option, value):
        if option == 'text_speed':
            self.text_speed = int(value)
        elif option == 'animation_speed':
            self.animation_speed = int(value)
        elif option == 'mute':
            self.mute = value

        #выполняются проверки, что бы нельзя было установить неподдерживаемые
        #значения
        if self.animation_speed > 50:
            self.animation_speed = 50
        elif self.animation_speed < 5:
            self.animation_speed = 5
        if self.text_speed > 500:
            self.text_speed = 500
        elif self.text_speed < 5:
            self.text_speed = 5

        self.settings.change_option(option, value) #записываю новое значение в settings.ini
        