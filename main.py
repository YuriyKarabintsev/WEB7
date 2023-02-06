import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
SCREEN_SIZE = [1500, 900]


class BigTask(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()
        print()


    def getImage(self):
        address_ll = "37.588392,55.734036"
        scale = 12
        response = requests.get(f"https://static-maps.yandex.ru/1.x/?ll={address_ll}&z={scale}&l=map&size=650,450")
        if not response:
            print("Ошибка выполнения запроса:")
            #print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
 
 
     def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Часть 1')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)  
        self.image.move(400, 0)
        self.image.resize(1500, 900)
        self.image.setPixmap(self.pixmap)


    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = BigTask()
    ex.show()
    sys.exit(app.exec())