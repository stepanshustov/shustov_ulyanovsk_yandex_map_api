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
        self.x = 48.38668
        self.y = 54.3282
        uic.loadUi('des.ui', self)
        self.type: QComboBox
        self.type.addItems(["схема", "спутник", "гибрид"])
        self.type.currentTextChanged.connect(self.repaint)
        self.info: QLabel
        self.d = {"схема": "map", "спутник": "sat ", "гибрид": "skl"}
        self.repaint()

    def repaint(self):
        self.type: QComboBox
        print(self.d[self.type.currentText()])
        params = {
            "ll": f"{self.x},{self.y}",
            "z": f"{self.z}",
            "l": f"{self.d[self.type.currentText()]}"
        }

        map_request = f"http://static-maps.yandex.ru/1.x"
        response = requests.get(map_request, params=params)

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
координаты: {self.x:.7},{self.y:.7}, МАШТАБ : {self.z}""")

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z = min(self.z + 1, 21)

        if event.key() == Qt.Key_PageDown:
            self.z = max(1, self.z - 1)
        if event.key() == Qt.Key_Right:
            self.x += 5000 / self.z ** 5
        if event.key() == Qt.Key_Left:
            self.x -= 5000 / self.z ** 5
        if event.key() == Qt.Key_Up:
            self.y += 2050 / self.z ** 5
        if event.key() == Qt.Key_Down:
            self.y -= 2050 / self.z ** 5

        self.x += 180
        self.x %= 360
        self.x -= 180

        self.y += 90
        self.y %= 180
        self.y -= 90

        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
