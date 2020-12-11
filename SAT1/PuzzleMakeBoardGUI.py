import sys
import numpy as np
import time
import os

from SAT1.FileOperation import FileOperation
import SAT1.MainGUI as mgui
from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication,
                             QLabel)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMenu, QGridLayout, QPushButton
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from functools import partial
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import QIcon, QPixmap


TREE=-1
EMPTY=0

class MakeBoard(QWidget):
    def __init__(self,x,y):
        super().__init__()
        self.row_size=int(x)
        self.column_size=int(y)
        self.environment = np.zeros((x, y))
        self.tree_label='T'
        self.init_ui()


    def init_ui(self):
        self.global_layout=QHBoxLayout()

        self.edit_platform_layout=QGridLayout()
        self.operate_platform_layout=QVBoxLayout()
        #
        self.row_all_cons=[]
        self.col_all_cons=[]
        for i in range(self.row_size+1):
            for j in range(self.column_size+1):
                if i!=self.row_size and j!=self.column_size:
                    button = QPushButton()
                    button.setObjectName('button_%d_%d'%(i,j))
                    button.setFixedSize(30,30)
                    button.clicked.connect(self.EnvAction)
                    self.edit_platform_layout.addWidget(button, i, j)
                elif i!=self.row_size and j==self.column_size:
                    row_cons=QLineEdit()
                    row_cons.setFixedSize(30,30)
                    row_cons.setObjectName('row_constraint_%d_%d'%(i,j))
                    self.row_all_cons.append(row_cons)
                    self.edit_platform_layout.addWidget(row_cons, i, j)
                elif i==self.row_size and j!=self.column_size:
                    col_cons = QLineEdit()
                    col_cons.setFixedSize(30, 30)
                    col_cons.setObjectName('row_constraint_%d_%d' % (i, j))
                    self.col_all_cons.append(col_cons)
                    self.edit_platform_layout.addWidget(col_cons, i, j)
                else:
                    pass
        #
        self.save_label=QLabel('Input save name:')
        self.save_state=QLabel('not saved')

        self.save_name_edit=QLineEdit()
        self.save_name_edit.setObjectName('file_name')

        self.save_button=QPushButton('Save')
        self.save_button.setObjectName('save_file_button')
        self.save_button.clicked.connect(self.SaveAction)

        self.operate_platform_layout.addWidget(self.save_state)
        self.operate_platform_layout.addWidget(self.save_label)
        self.operate_platform_layout.addWidget(self.save_name_edit)
        self.operate_platform_layout.addWidget(self.save_button)

        ggwg=QWidget()
        vgwg=QWidget()

        ggwg.setLayout(self.edit_platform_layout)
        vgwg.setLayout(self.operate_platform_layout)

        self.global_layout.addWidget(ggwg)
        self.global_layout.addWidget(vgwg)

        self.setLayout(self.global_layout)
        self.setWindowTitle('Puzzle Maker')
        self.Centralization()
        self.show()

    def Centralization(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def SaveAction(self):
        row_cons=[]
        col_cons=[]
        file_name=self.save_name_edit.text()
        for r in self.row_all_cons:
            temp=r.text()
            if not self.is_number(temp):
                QMessageBox.warning(self, "Warning", "Row constrains must be integer", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.Yes)
                break
            else:
                if temp!=None:
                    row_cons.append(int(temp))
        for c in self.col_all_cons:
            temp=c.text()
            if not self.is_number(temp):
                QMessageBox.warning(self, "Warning", "Column constrains must be integer", QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.Yes)
                break
            else:
                if temp!=None:
                    col_cons.append(int(temp))
        prefix='env'
        suffix=''
        type='.txt'
        if file_name=='':
            QMessageBox.warning(self, "Warning", "File name is empty", QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.Yes)
        else:
            path = os.path.join(prefix, 'tents'+file_name+'-%dx%d'%(int(self.row_size),int(self.column_size))+'-mk'+type)
            with open(path, "w") as f:
                    f.write(str(self.row_size)+' '+str(self.column_size)+'\n')
                    for i in range(self.row_size):
                        for j in range(self.column_size+2):
                            if j<self.column_size:
                                if self.environment[i,j]==-1:
                                    f.write('T')
                                else:
                                    f.write('.')
                            elif j==self.column_size:
                                f.write(' ')
                            else:
                                f.write(str(row_cons[i])+'\n')
                    for i in range(len(col_cons)-1):
                        f.write(str(col_cons[i])+' ')
                    f.write(str(col_cons[-1]))
            f.close()
            self.save_state.setText('save successed')
            time.sleep(1)
            self.close()
            default_file_name = 'tents-8x8-t1.txt'
            name = default_file_name.split('.')[0]
            map = FileOperation.ReadFile(default_file_name)
            self.b_gui = mgui.GUI(map, name)


        # print(row_cons)
        # print(col_cons)
        # self.close()
        # self.make_board =

    def EnvAction(self):
        sender=self.sender()
        objname = str(sender.objectName())
        name_list = objname.split('_')[-2:]
        positon = [int(i) for i in name_list]
        x=positon[0]
        y=positon[1]
        if sender.text()==self.tree_label:
            sender.setText('')
            self.environment[x,y]=EMPTY
        else:
            sender.setText('T')
            self.environment[x,y]=TREE

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
    gui = MakeBoard(2,2)
    sys.exit(app.exec_())
