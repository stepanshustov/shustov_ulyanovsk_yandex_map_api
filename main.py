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
        self.z = 9
        uic.loadUi('des.ui', self)
        self.repaint()
        self.info: QLabel

    def repaint(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll=48.38668,54.3282&z={self.z}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)
        self.info.setText(f"""Ульяновск, тип карты: спутник,
координаты: 48.38668,54.3282, МАШТАБ : {self.z}""")

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z = min(self.z + 1, 21)
            self.repaint()
        if event.key() == Qt.Key_PageDown:
            self.z = max(1, self.z - 1)
            self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
