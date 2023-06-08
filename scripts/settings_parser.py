'''класс реализует считывание из файла settings.ini настроек, и передаче
их игре'''

class SettingsParser():
    def __init__(self):
        pass

    def parse(self):
        try:
            #пытаюсь открыть файл настроек
            file = open('settings.ini', 'r')
        except:
            #если не нахожу его, записываю файл с дефолтными настройками
            file = open('settings.ini', 'w')
            file.write('animation_speed=20\ntext_speed=50\nmute=false')
            file.close()
            file = open('settings.ini', 'r')

        settings = file.read()
        file.close()
        temp = settings.split('\n')

        #дефолтные настройки
        animation_speed = 13
        text_speed = 50
        mute = 'false'

        for option in temp:
            if 'animation_speed' in option:
                animation_speed = int(option.split('=')[1])
            if 'text_speed' in option:
                text_speed = int(option.split('=')[1])
            if 'mute' in option:
                mute = option.split('=')[1]

        #выполняются проверки, что бы нельзя было установить неподдерживаемые
        #значения
        if animation_speed > 50:
            animation_speed = 50
            self.change_option('animation_speed', '50')
        elif animation_speed < 5:
            animation_speed = 5
            self.change_option('animation_speed', '5')
        if text_speed > 500:
            text_speed = 500
            self.change_option('text_speed', '500')
        elif text_speed < 5:
            text_speed = 5
            self.change_option('text_speed', '5')

        return animation_speed, text_speed, mute

    def change_option(self, name, value):
        '''изменяет значение указанного по имени параметра'''
        #проверка, если были переданы значения выходящие за допустимые пределы,
        #записываю максимальные/минимальные значения
        if name == 'text_speed' and int(value)>500:
            value=500
        elif name == 'text_speed' and  int(value)<5:
            value=5
        if name == 'animation_speed' and int(value)>50:
            value=50
        elif name == 'animation_speed' and int(value)<5:
            value=5

        file = open('settings.ini', 'r')
        temp_options = file.read()
        options = ''
        file.close()

        for option in temp_options.split('\n'):
            if name in option:
                options+=name+'='+str(value)+'\n'
            else:
                options+=option+'\n'

        file = open('settings.ini', 'w')
        file.write(options)
        file.close()

    def get_option_value(self, name):
        '''возвращает значение указанного параметра'''
        file = open('settings.ini', 'r')
        temp_options = file.read()
        options = ''
        file.close()

        value=False

        for option in temp_options.split('\n'):
            if name in option:
                value=option.split('=')[1]
        return value
