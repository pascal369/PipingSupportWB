# -*- coding: utf-8 -*-

import os
from re import X
import sys
#from tkinter import W
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
from FreeCAD import Base
import FreeCAD, Part, math
import DraftVecUtils
import Sketcher
import PartDesign
from math import pi
import Draft
import FreeCAD as App
import FreeCADGui as Gui
from pspt_data import ParamS01
from pspt_data import ParamS02
from pspt_data import ParamS04
from pspt_data import ParamS05
from pspt_data import ParamS06
from pspt_data import ParamS08
from pspt_data import ParamS10
from pspt_data import psuport_data
DEBUG = True
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 120)
        Dialog.move(800, 0)
        #形式
        self.label = QtGui.QLabel('形式',Dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 81, 22))
        self.label.setStyleSheet("color: black;")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(100, 0, 100, 20))
        self.comboBox.setObjectName("comboBox")
        #形鋼
        self.label_3 = QtGui.QLabel('形鋼',Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 25, 81, 22))
        self.label_3.setStyleSheet("color: black;")
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(100, 28, 100, 20))
        self.comboBox_3.setMaxVisibleItems(10)
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(220, 0, 130, 110))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        #実行      
        self.pushButton = QtGui.QPushButton('実行',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 70, 70, 22))
        self.pushButton.setObjectName("pushButton")
        self.comboBox.addItems(psuport_data.type)
        self.comboBox_3.addItems(psuport_data.katakou)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.onType)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(1)
        self.comboBox_3.currentIndexChanged[int].connect(self.onKatakou)
        self.comboBox_3.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def Import(self):
         global selected_object
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             self.comboBox.setCurrentText(selected_object.Type)   
             self.comboBox_3.setCurrentText(selected_object.ShapedSteel)  
    def onType(self):
        global key
        global key1
        self.comboBox_3.clear()
        key = self.comboBox.currentIndex()
        key1=self.comboBox_3.currentIndex()
        if key==0:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_01_a'
        elif key==1:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_02_a'
        elif key==2:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_03_a'
        elif key==3:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_04_a'
        elif key==4:
            self.comboBox_3.addItems(psuport_data.katakou[2:3])
            img='s_05_a'
        elif key==5:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_06_a'
        elif key==6:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_07_a'
        elif key==7:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_08_a'
        elif key==8:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_09_a'
        elif key==9:
            self.comboBox_3.addItems(psuport_data.sichu)
            img='s_10_a'
        if key==9:
            self.comboBox_5.setCurrentIndex(3)
        pic=img + '.jpg'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "pspt_data",pic)
        self.label_7.setPixmap(QtGui.QPixmap(joined_path))
    def onKatakou(self):
        global key1
        global katakou_size
        key1=self.comboBox_3.currentIndex()
        if key<=8:
            if key==4:
                katakou_size=psuport_data.RB_ss_size
            else:
                if key1==0:
                    katakou_size=psuport_data.angle_ss_size
                elif key1==1:
                    katakou_size=psuport_data.channel_ss_size
        elif key==9:
            if key1==0:#支柱
                katakou_size=psuport_data.SGP_size
            elif key1==1:#笠木
                katakou_size=psuport_data.channel_ss_size

        self.comboBox_4.clear()
        self.comboBox_4.addItems(katakou_size)
    def create(self):
        if key==0:#S01
            if key1==0: #アングル
                fname='s01_angle.FCStd'
            elif key1==1:
                fname='s01_channel.FCStd'
                   
        elif key==1 or key==2:#S02 S03
            if key==1:
                if key1==0: #アングル
                    fname='s02_angle.FCStd'
                elif key1==1:
                    fname='s02_channel.FCStd'
            elif key==2:
                if key1==0: #アングル
                    fname='s03_angle.FCStd'
                elif key1==1:
                    fname='s03_channel.FCStd'        
        elif key==3:#S04
            if key1==0: #アングル
                fname='s04_angle.FCStd'
            elif key1==1:
                fname='s04_channel.FCStd'
        elif key==4:#05
            fname='s05_support.FCStd'
        elif key==5 or key==6:#s06 s07
            if key==5:
                if key1==0: #アングル
                    fname='s06_angle.FCStd'
                elif key1==1:
                    fname='s06_channel.FCStd'
            elif key==6:
                if key1==0: #アングル
                    fname='s07_angle.FCStd'
                elif key1==1:
                    fname='s07_channel.FCStd'    
        elif key==7 or key==8:#s08 s09
            if key==7:
                if key1==0: #アングル
                    fname='s08_angle.FCStd'
                elif key1==1:
                    fname='s08_channel.FCStd'
            elif key==8:
                if key1==0: #アングル
                    fname='s09_angle.FCStd'
                elif key1==1:
                    fname='s09_channel.FCStd'   
        elif key==9:
            fname='s10_support.FCStd'
        try:
            base=os.path.dirname(os.path.abspath(__file__))
            joined_path = os.path.join(base, 'pspt_data',fname) 
            Gui.ActiveDocument.mergeProject(joined_path) 
        except:
            pass       
class main():
        w = QtGui.QWidget()
        w.ui = Ui_Dialog()
        w.ui.setupUi(w)
        w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        w.show()

 
   
