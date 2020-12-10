
# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import time

from SAT1.GridMaker import GridMaker
from SAT1.FileOperation import FileOperation
from SAT1.Solver import SAT1Solver
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

class GUI(QWidget):

    def __init__(self,map:dict,name:str):
        super().__init__()
        # the structure of result is like ['environment','size','row_number','column_number']
        self.DataInput(map,name)
        self.InitUI()

    def DataInput(self,map:dict,name):
        self.data = map
        self.size = map['size']
        self.row_number = map['row_number']
        self.column_number = map['column_number']
        self.envrionment = map['environment']
        self.name=name

    def Centralization(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closewin(self):
        self.close()

    def InitUI(self):
        self.wlayout=QHBoxLayout()
        self.vlayout=QVBoxLayout()
        self.glayout = QGridLayout()

        #grid setting
        #environment
        positions = [(i, j) for i in range(self.size[0]+1) for j in range(self.size[1]+1)]
        env=list(self.envrionment.flat)
        for i in range(len(env)):
            if env[i]==-1:
                env[i]='T'
            elif env[i]==0:
                env[i]=''
        env=np.array(env).reshape((self.size[0],self.size[1]))
        for i in range(self.size[0]+1):
            for j in range(self.size[1]+1):
                if i!=self.size[0] and j!=self.size[1]:
                    button = QPushButton(env[i,j])
                    button.setObjectName('button_%d_%d'%(i,j))
                    button.setFixedSize(30,30)
                    self.glayout.addWidget(button, i, j)
                elif i!=self.size[0] and j==self.size[1]:
                    label=QLabel(self)
                    label.setFixedSize(10,30)
                    label.setText(str(self.row_number[i]))
                    self.glayout.addWidget(label, i, j)
                elif i==self.size[0] and j!=self.size[1]:
                    label=QLabel(self)
                    label.setFixedSize(30, 10)
                    label.setAlignment(Qt.AlignCenter)
                    label.setText(str(self.column_number[j]))
                    self.glayout.addWidget(label, i, j)
                else:
                    pass
        #vlayout setting
        self.solve_button=QPushButton('Solve')
        self.solve_button.setObjectName('solve_button')
        self.solve_button.clicked.connect(self.Solve)

        self.load_button=QComboBox()
        self.load_button.setObjectName('load_button')
        self.LoadItemsetting()
        self.load_button.currentTextChanged.connect(self.LoadAction)

        self.auto_make_butoon=QComboBox()
        self.auto_make_butoon.setObjectName('auto_make_button')
        self.AutoMakerItemSetting()
        self.auto_make_butoon.currentTextChanged.connect(self.AutoMakerAction)

        self.vlayout.addWidget(self.solve_button)
        self.vlayout.addWidget(self.auto_make_butoon)
        self.vlayout.addWidget(self.load_button)


        gwg = QWidget()
        vwg = QWidget()

        gwg.setLayout(self.glayout)
        vwg.setLayout(self.vlayout)
        #
        self.wlayout.addWidget(gwg)
        self.wlayout.addWidget(vwg)

        self.setLayout(self.wlayout)
        #

        self.setWindowTitle(self.name)
        self.Centralization()
        self.show()


    def LoadItemsetting(self):
        self.file_list=FileOperation.GetFileNameList()
        self.load_button.addItems(self.file_list)

    def LoadAction(self,file_name):
        self.closewin()
        newfile_name = file_name
        new_name = file_name.split('.')[0]
        map = FileOperation.ReadFile(newfile_name)
        self.new_gui = GUI(map, new_name)


    def Solve(self):
        sol=SAT1Solver(self.data)
        sol.Run()
        sol_list=sol.result
        sol_tag=sol.result_tag
        if sol_tag==False:
            QMessageBox.warning(self,"Result","Not solveable",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        else:
            for position in sol_list:
                x=int(position[0])
                y=int(position[1])
                name = self.glayout.itemAtPosition(x,y).widget().objectName()
                item = self.findChild(QPushButton, name)
                item.setText('O')

    def AutoMakerItemSetting(self):
        item=['none','8x8','10x10','15x10','25x25','30x30']
        self.auto_make_butoon.addItems(item)

    def AutoMakerAction(self,k):
        if k=='none':
            pass
        else:
            size=k.split('x')
            i=int(size[0])
            j=int(size[1])
            gridmaker=GridMaker(i,j)
            new_map=gridmaker.data
            time.sleep(0.2)
            self.closewin()
            time.sleep(0.1)
            self.auto_puzzle=GUI(new_map,'auto'+k)

if __name__ == '__main__':
    file_name = 'tents-8x8-t1.txt'
    name=file_name.split('.')[0]
    map = FileOperation.ReadFile(file_name)
    app = QApplication(sys.argv)
    gui = GUI(map,name)
    sys.exit(app.exec_())


