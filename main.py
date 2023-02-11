import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
SCREEN_SIZE = [1500, 900]


class BigTask(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 12
        self.scale_max = 21
        self.scale_min = 1
        self.getImage(scale=self.scale)
        self.initUI()

    def getImage(self, scale):
        if self.scale_min <= scale <= self.scale_max:
            address_ll = "37.588392,55.734036"
            response = requests.get(f"https://static-maps.yandex.ru/1.x/?ll={address_ll}&z={scale}&l=map&size=650,450")
            if not response:
                print("Ошибка выполнения запроса:")
                #print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
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
        # Обработка нажатия клавиш PgUp и PgDown:
        # PgUp - параметр масштаба увеличивается
        # PgDown - параметр масштаба уменьшается
        if event.key() == Qt.Key_PageUp:
            if self.scale < self.scale_max:
                self.scale += 1
        elif event.key() == Qt.Key_PageDown:
            if self.scale > self.scale_min:
                self.scale -= 1
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