import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication,QWidget
from PyQt5.QtCore import QCoreApplication


class First(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    def closewin(self):
        self.close()

    def initUI(self):
        self.btn = QPushButton("Button", self)
        self.btn.move(30, 50)

        self.btn.clicked.connect(self.action)
        self.btn.clicked.connect(QCoreApplication.instance().quit)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Event sender')
        self.show()

    def action(self):
        b = Second()
        b.show()



class Second(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Get sender')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = First()

    sys.exit(app.exec_())