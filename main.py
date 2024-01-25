import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import os

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('des.ui', self)
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)
        self.info: QLabel
        self.info.setText("Ульяновск, тип карты: спутник, координаты: 48.38668,54.3282")

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll=48.38668,54.3282&spn=0.7,0.7&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
