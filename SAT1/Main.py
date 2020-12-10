import sys
from PyQt5.QtWidgets import QApplication
from SAT1.GUI import GUI
from SAT1.FileOperation import FileOperation

if __name__ == '__main__':
    default_file_name = 'tents-8x8-t1.txt'
    name=default_file_name.split('.')[0]
    map = FileOperation.ReadFile(default_file_name)
    app = QApplication(sys.argv)
    gui = GUI(map,name)
    sys.exit(app.exec_())