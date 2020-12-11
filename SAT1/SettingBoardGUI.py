import sys
import numpy as np
import time
import os


from SAT1.FileOperation import FileOperation
from SAT1.PuzzleMakeBoardGUI import MakeBoard

from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication,
                             QLabel)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMenu,QGridLayout,QPushButton
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from functools import partial
from PyQt5.QtWidgets import  QPushButton,QVBoxLayout,QWidget,QApplication
from PyQt5.QtGui import QIcon,QPixmap

class ManualBoard(QWidget):
    def __init__(self):
        super().__init__()
        # super()方法返回了父类对象并调用了父类的构造方法
        self.__init_ui()

    def __init_ui(self):
        self.whole_layout = QVBoxLayout()
        self.manual_size_board = QHBoxLayout()
        #
        self.x_label = QLabel('x size:')
        self.x_input = QLineEdit()
        self.x_input.setObjectName('x_input')

        self.y_label = QLabel('y size:')
        self.y_input = QLineEdit()
        self.y_input.setObjectName('y_input')

        self.manual_size_board.addWidget(self.x_label)
        self.manual_size_board.addWidget(self.x_input)
        self.manual_size_board.addWidget(self.y_label)
        self.manual_size_board.addWidget(self.y_input)

        hgwg = QWidget()
        hgwg.setLayout(self.manual_size_board)
        #
        self.confirm_button = QPushButton('Confirm')
        self.confirm_button.setObjectName('confirm_button')
        self.confirm_button.clicked.connect(self.ConfirmAction)

        self.whole_layout.addWidget(hgwg)
        self.whole_layout.setSpacing(20)
        self.whole_layout.addWidget(self.confirm_button)
        #
        self.setLayout(self.whole_layout)
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Size Setting')
        self.Centralization()
        self.show()

    def Centralization(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ConfirmAction(self):
        tag=False
        x=self.x_input.text()
        y=self.y_input.text()
        if not self.is_number(x) or not self.is_number(y):
            pass
        elif int(x)<0 or int(y)<0:
            pass
        else:
            tag=True
            x=int(x)
            y=int(y)

        if tag:
            if x>=35 and y>=35:
                QMessageBox.warning(self, "Warning", "Oversize (not over 35)", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.Yes)
            else:
                self.close()
                self.board=MakeBoard(x,y)
        else:
            QMessageBox.warning(self, "Waring", "Not Valid Input", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ManualBoard()
    sys.exit(app.exec_())

