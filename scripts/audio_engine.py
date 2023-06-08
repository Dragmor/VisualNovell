'''класс отвечает за воспроизведение музыки
    self.window.audio.play('sounds/1', loop=True) #запускает зацикленное воспроизведение файла sounds.1.wav
    self.window.audio.play('sounds/1') #единоразовое воспроизведение файла
    self.window.audio.stop() #останавливает воспроизведение играющего файла!
    '''

import winsound
import multiprocessing

from scripts.settings_parser import *

class AudioPlayer():
    def __init__(self):
        '''что бы воспроизвести последний запускаемый луп-файл, нужно обратиться
        к переменной self.last_playing'''
        self.start = multiprocessing.Process()
        self.settings_parser = SettingsParser() #парсер, используется для проверки
            #состояния mute
        self.last_playing = '' #последний воспроизводимый файл, нужен что бы 
            #при включении звука включать последний файл, если он цикличный

    def play(self, fname='', loop=False):
        '''метод запускает в процессе воспроизведение музыки. Если loop==True,
        то воспроизводится будет в цикле, если False, то после окончания музыки
        останавливается'''
        if loop:
            if self.last_playing == fname and self.start.is_alive(): #если пытается воспроизвести зацикленно файл,
                #который по идее и так сейчас играет, то выхожу отсюда
                return
            else:
                self.last_playing = fname #записываю название последнего воспроизводимаго луп файла

        if self.settings_parser.get_option_value('mute') == 'true':
            pass
        else:
            if loop: #если нужно играть в цикле, то..
                self.stop() #нужно, если уже играет луп-файл, и передан ещё один, не идентичный играющему
                self.start = multiprocessing.Process(target=self.start_play, args=(True, fname))
            else: #если же нужно проиграть единоразово
                self.start = multiprocessing.Process(target=self.start_play, args=(False, fname))
            self.start.daemon = True
            self.start.start()


    def start_play(self, loop=False, fname='', *args):
        '''в цикле воспроизводит музыку с названием fname'''
        while loop: #если нужно играть в цикле
            winsound.PlaySound(fname+'.wav', winsound.SND_ALIAS) #запуск воспроизведения
        winsound.PlaySound(fname+'.wav', winsound.SND_ALIAS)

    def play_last_loop(self):
        '''метод воспроизводит аудиофайл, который имеет флаг луп и
        запускался последним'''
        self.play(fname=self.last_playing, loop=True)

    def stop(self):
        '''закрываю процесс воспроизведения файла'''
        try:
            self.start.terminate() #завершаю процесс проигрывания аудиофайла
        except:
            pass
