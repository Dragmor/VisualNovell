import sqlite3


class ScenarioDB():
    '''класс отвечает за извлечение сцен из БД'''
    def __init__(self):
        #подключаюся к БД сцен
        self.database = sqlite3.connect('scenario/scenes.db')
        self.cursor = self.database.cursor()

    def get_scene(self, scene_id):
        '''возвращает указанныю сцену'''
        self.cursor.execute('''SELECT type FROM scenes WHERE scene_id=%s''' %scene_id)
        data = self.cursor.fetchone()
        if data[0] == 'exit':
            return 'exit', 'exit'
        self.cursor.execute('''SELECT * FROM %s WHERE scene_id=%s''' %(data[0], scene_id))
        scene = self.cursor.fetchone()
        return data[0], scene #возвращает инфо о сцене
