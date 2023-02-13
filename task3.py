import os
import sys
import requests
from datetime import datetime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [1500, 900]



class BigTask(QWidget):
    scale = 12
    scale_max = 21
    scale_min = 1
    x_ll = 37.588392
    y_ll = 55.734036
    def __init__(self):
        super().__init__()
        self.getImage(scale=self.scale)
        self.initUI()


    def getImage(self, scale):
        if self.scale_min <= scale <= self.scale_max:
            quest = f"https://static-maps.yandex.ru/1.x/?apikey='40d1649f-0493-4b70-98ba-98533de7710b'&ll={str(self.x_ll) + ',' + str(self.y_ll)}&z={scale}&l=map&size=650,450"
            response = requests.get(quest)
            if not response:
                print("Ошибка выполнения запроса:", quest)
                #print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                print('Time:', datetime.now())
                sys.exit(1)
            self.map_file = f"map{scale}.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
 
 
    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Часть 2')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)  
        self.image.move(400, 0)
        self.image.resize(1500, 900)
        self.image.setPixmap(self.pixmap)
        self.image.show()
        os.remove(self.map_file)


    def keyPressEvent(self, event):
        print('keyPressEvent', event.key(), datetime.now())
        # Обработка нажатия клавиш PgUp и PgDown:
        # PgUp - параметр масштаба увеличивается
        # PgDown - параметр масштаба уменьшается
        if event.key() == Qt.Key_PageUp:
            if self.scale < self.scale_max:
                self.scale += 1
        elif event.key() == Qt.Key_PageDown:
            if self.scale > self.scale_min:
                self.scale -= 1

        if event.key() == 16777236:
            self.x_ll += 0.1 / self.scale
        elif event.key() == 16777234:
            self.x_ll -= 0.1 / self.scale

        if event.key() == 16777235:
            self.y_ll += 0.1 / self.scale
        elif event.key() == 16777237:
            self.y_ll -= 0.1 / self.scale
        # Скачивание картинки с нужным масштабом
        self.getImage(scale=self.scale)
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(400, 0) # позиционирование картинки в нужном месте в окне программы
        self.image.resize(1500, 900) # изменение размера картинки
        self.image.setPixmap(self.pixmap)
        self.image.show() # показ картинки (без этой команды остаётся старая картинка)
        os.remove(self.map_file) # удаление файла картинки, чтобы не засорять память


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BigTask()
    ex.show()
    sys.exit(app.exec())