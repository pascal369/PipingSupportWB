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
        Dialog.resize(365, 315)
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
        #形鋼サイズ
        self.label_8 = QtGui.QLabel('形鋼サイズ',Dialog)
        self.label_8.setGeometry(QtCore.QRect(10, 55, 81, 22))
        self.label_8.setStyleSheet("color: black;")
        self.comboBox_4 = QtGui.QComboBox(Dialog)
        self.comboBox_4.setGeometry(QtCore.QRect(100, 55, 100, 20))
        self.comboBox_4.setMaxVisibleItems(10)
        self.comboBox_4.setObjectName("comboBox_4")
        #スパンL
        self.label_2 = QtGui.QLabel('スパンL[mm]',Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 81, 22))
        self.label_2.setStyleSheet("color: black;")
        self.lineEdit_L = QtGui.QLineEdit('300',Dialog)
        self.lineEdit_L.setGeometry(QtCore.QRect(100, 83, 69, 22))
        self.lineEdit_L.setObjectName("lineEdit")
        #垂直材
        #H(mm)
        self.label_5 = QtGui.QLabel('H[mm]',Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 105, 81, 22))
        self.label_5.setStyleSheet("color: black;")
        self.lineEdit = QtGui.QLineEdit('300',Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 108, 71, 22))
        self.lineEdit.setObjectName("lineEdit")
        #H1(mm)
        self.label_6 = QtGui.QLabel('H1[mm]',Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 130, 81, 22))
        self.label_6.setStyleSheet("color: black;")
        self.lineEdit_2 = QtGui.QLineEdit('300',Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 133, 71, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        #斜材角度
        self.label_k = QtGui.QLabel('斜材角度[deg]',Dialog)
        self.label_k.setGeometry(QtCore.QRect(10, 160, 81, 22))
        self.label_k.setStyleSheet("color: black;")
        self.comboBox_k = QtGui.QComboBox(Dialog)
        self.comboBox_k.setGeometry(QtCore.QRect(100, 160, 71, 22))
        self.comboBox_k.setObjectName("comboBox_k")
        #ベースプレート
        #checkbox
        self.checkbox = QtGui.QCheckBox('ベースプレート',Dialog)
        self.checkbox.setGeometry(QtCore.QRect(210, 0, 130, 22))
        self.checkbox.setObjectName("checkbox")
        self.checkbox.setChecked(True)
        self.checkbox.setStyleSheet("color: black;")

        #板厚
        self.label_10 = QtGui.QLabel('板厚[mm]',Dialog)
        self.label_10.setGeometry(QtCore.QRect(210, 25, 71, 22))
        self.label_10.setStyleSheet("color: black;")
        self.comboBox_5 = QtGui.QComboBox(Dialog)
        self.comboBox_5.setGeometry(QtCore.QRect(280, 25, 69, 22))
        self.comboBox_5.setMaxVisibleItems(10)
        self.comboBox_5.setObjectName("comboBox_5")
        #横幅
        self.label_x = QtGui.QLabel('X[mm]',Dialog)
        self.label_x.setGeometry(QtCore.QRect(210, 50, 71, 22))
        self.label_x.setStyleSheet("color: black;")
        self.lineEdit_x = QtGui.QLineEdit('',Dialog)
        self.lineEdit_x.setGeometry(QtCore.QRect(280, 53, 71, 22))
        #縦長
        self.label_y = QtGui.QLabel('Y[mm]',Dialog)
        self.label_y.setGeometry(QtCore.QRect(210, 80, 71, 22))
        self.label_y.setStyleSheet("color: black;")
        self.lineEdit_y = QtGui.QLineEdit('',Dialog)
        self.lineEdit_y.setGeometry(QtCore.QRect(280, 80, 71, 22))
        #img
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(220, 130, 130, 110))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        #実行      
        self.pushButton = QtGui.QPushButton('実行',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 250, 70, 22))
        self.pushButton.setObjectName("pushButton")
        
        self.comboBox.addItems(psuport_data.type)
        self.comboBox_k.addItems(psuport_data.kaku)
        self.comboBox_3.addItems(psuport_data.katakou)
        self.comboBox_5.addItems(psuport_data.ita_t)
        self.comboBox_5.setCurrentIndex(3)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.onType)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(1)
        self.comboBox_3.currentIndexChanged[int].connect(self.onKatakou)
        self.comboBox_3.currentIndexChanged[int].connect(self.onSize)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(1)
        self.comboBox_4.currentIndexChanged[int].connect(self.onSize)
        self.comboBox_4.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def Import(self):
         global selected_object
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             self.comboBox.setCurrentText(selected_object.Type)   
             self.comboBox_3.setCurrentText(selected_object.ShapedSteel)  
             self.comboBox_4.setCurrentText(selected_object.size)   
        
    def onType(self):
        global key
        global key1
        self.comboBox_3.clear()
        key = self.comboBox.currentIndex()
        key1=self.comboBox_3.currentIndex()

        if key==0:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_01_a'
            self.lineEdit_2.setText('')
            self.lineEdit_2.setEnabled(False)
            self.label_6.setText('')

        elif key==1:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_02_a'

            if key1==0:
                self.lineEdit_2.setText('')
                self.lineEdit_2.setEnabled(False)
                self.label_6.setText('')
            elif key1==10:
                self.lineEdit_2.setEnabled(True)
                self.lineEdit_2.setText('150')
        elif key==2:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_03_a'
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_2.setText('150')
            self.label_5.setText('H[mm]')
            self.label_6.setText('H1[mm]')
        elif key==3:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_04_a'
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('')
            self.label_6.setText('')
        elif key==4:
            self.comboBox_3.addItems(psuport_data.katakou[2:3])
            img='s_05_a'
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.label_5.setText('')
            self.label_6.setText('')
            self.label_2.setText('H[mm]')
        elif key==5:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_06_a'
            self.lineEdit.setText('500')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setText('L[mm}')
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('')
        elif key==6:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_07_a'
            self.lineEdit.setText('500')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setText('200')
            self.lineEdit_2.setEnabled(True)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('H1[mm]')
        elif key==7:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_08_a'
            self.lineEdit_2.setText('')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('')
        elif key==8:
            self.comboBox_3.addItems(psuport_data.katakou[:2])
            img='s_09_a'
            self.lineEdit_2.setText('200')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.label_5.setText('H[mm]')
            self.label_6.setText('H1[mm]')
        elif key==9:
            self.comboBox_3.addItems(psuport_data.sichu)
            img='s_10_a'
            self.lineEdit.setText('1000')
            self.lineEdit_2.setText('')
            self.lineEdit_2.setEnabled(False)
            self.label_2.setText('L[mm]')
            self.label_5.setText('H[mm]')
            self.label_6.setText('')
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

    def onSize(self):
        global size
        global sa
        global sa2
        global size1
        global size2
        global W
        global B
        size=self.comboBox_4.currentText()
        if key<=8:
            katakou=self.comboBox_3.currentText()
            if key1==0:
                try:
                    sa=psuport_data.angle_ss_equal[size]
                except:
                    pass

                A=sa[0]
                W=A+50
                B=A+20
                self.lineEdit_x.setText(str(W))
                self.lineEdit_y.setText(str(B))

            elif key1==1:
                
                try:
                    sa=psuport_data.channel_ss[size]
                except:
                    pass   
                W=sa[0]+50
                B=sa[1] +20
                self.lineEdit_x.setText(str(W))
                self.lineEdit_y.setText(str(B))
            elif key1==2:
                sa=psuport_data.STK_ss[size]
                W=sa[0]
                B=sa[1]     
            else:
                pass

            if key1==0:
                try:
                    sa=psuport_data.angle_ss_equal[size]
                except KeyError:
                    pass
            elif key1==1:
                try:
                    sa=psuport_data.channel_ss[size]
                except KeyError:
                    pass
        elif key==9:
            
            try:
                if key1==0:
                    #size1=size
                    sa=psuport_data.SGP[size]
                elif key1==1:
                    #size2=size
                    sa=psuport_data.channel_ss[size]
                self.lineEdit_x.setText('200')
                self.lineEdit_y.setText('')    
            except:
                pass
    def create(self):
    #    global L
    #    global x0
    #    global c1
    #    global vx
    #    global vy
    #    global vz
    #    global A
    #    global t
    #    global w0
    #    global h0
    #    global pface_c
    #    global D
    #    global t0
    #    global sa
#
    #    x0=1
    #    vz=1
    #    key = self.comboBox.currentIndex()
    #    key1=self.comboBox_3.currentIndex()
    #    Type=self.comboBox.currentText()
    #    label=Type
    #    if key==3:
    #        pass
    #    else:
    #        obj = App.ActiveDocument.addObject("Part::FeaturePython",label)
    #        obj.addProperty("App::PropertyString", "Type",'Type').Type=Type
    #    #print(Type)
        if key==0:#S01
            #katakou=self.comboBox_3.currentText()
            #if self.checkbox.isChecked():
            #    obj.addProperty("App::PropertyBool", "BasePlate",'BasePlate').BasePlate = True 
            #else:    
            #    obj.addProperty("App::PropertyBool", "BasePlate",'BasePlate').BasePlate = False  
            #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou

            #if key1==0:#アングル
            if key1==0: #アングル
                fname='s01_angle.FCStd'
            elif key1==1:
                fname='s01_channel.FCStd'
            #base=os.path.dirname(os.path.abspath(__file__))
            #joined_path = os.path.join(base, 'pspt_data',fname) 
            #Gui.ActiveDocument.mergeProject(joined_path)
            #return    
                #L1=float(self.lineEdit_L.text())
                #H=float(self.lineEdit.text())
                #t0=float(self.comboBox_5.currentText())
                #sa=psuport_data.angle_ss_equal[size]
                #a=sa[0]
                #b=sa[1]
                #A=a
                #W=A+50
                #B=A+20
                #obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
                #obj.addProperty("App::PropertyFloat", "H0",'Dimension').H0=H
                #obj.addProperty("App::PropertyFloat", "b",'BasePlate').b=b
                #obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
                #obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
                #obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
                #obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B
#
                #obj.size=psuport_data.angle_ss_size
                #i=self.comboBox_4.currentIndex()
                #obj.size=psuport_data.angle_ss_size[i] 
                #ParamS01.S01(obj) 
                #obj.ViewObject.Proxy=0

            #elif key1==1:#チャンネル
            #    L1=float(self.lineEdit_L.text())
            #    t0=float(self.comboBox_5.currentText())
#
            #    H=float(self.lineEdit.text())
            #    W=float(self.lineEdit_x.text())
            #    B=float(self.lineEdit_y.text())
            #    obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
            #    obj.addProperty("App::PropertyFloat", "H0",'Dimension').H0=H
            #    obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
            #    obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
            #    obj.addProperty("App::PropertyFloat", "W",'BasePlate')
            #    obj.addProperty("App::PropertyFloat", "B",'BasePlate')
            #    obj.addProperty("App::PropertyFloat", "b",'Dimension')
#
            #    obj.size=psuport_data.channel_ss_size
            #    i=self.comboBox_4.currentIndex()
            #    obj.size=psuport_data.channel_ss_size[i] 
            #    ParamS01.S01(obj) 
            #    obj.ViewObject.Proxy=0
                    
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

                
            #katakou=self.comboBox_3.currentText()
            #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
            #if key1==0:#アングル
            #    
            #    if self.checkbox.isChecked():
            #        obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
            #    else:    
            #        obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
#
            #    L1=float(self.lineEdit_L.text())
            #    H=float(self.lineEdit.text())
            #    obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
            #    obj.addProperty("App::PropertyFloat", "H0",'Dimension').H0=H
            #    obj.addProperty("App::PropertyFloat", "b",'Dimension')
            #    if key==2:
            #        H1=float(self.lineEdit_2.text())
            #        obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
#
            #    W=float(self.lineEdit_x.text())
            #    B=float(self.lineEdit_y.text())    
            #    obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            #    obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B    
            #    t0=float(self.comboBox_5.currentText())
            #    obj.addProperty("App::PropertyFloat", "t0","BasePlate").t0=t0
            #    obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
#
            #    obj.size=psuport_data.angle_ss_size
            #    i=self.comboBox_4.currentIndex()
            #    obj.size=psuport_data.angle_ss_size[i] 
            #    ParamS02.S02(obj) 
            #    obj.ViewObject.Proxy=0
            #    
            #elif key1==1:#チャンネル
            #    if self.checkbox.isChecked():
            #        obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
            #    else:    
            #        obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
#
            #    L1=float(self.lineEdit_L.text())
            #    H=float(self.lineEdit.text())
            #    t0=float(self.comboBox_5.currentText())
            #    W=float(self.lineEdit_x.text())
            #    B=float(self.lineEdit_y.text())    
            #    obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            #    obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B  
            #    obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
            #    obj.addProperty("App::PropertyFloat", "H0",'Dimension').H0=H
            #    obj.addProperty("App::PropertyFloat", "b",'Dimension')
            #    obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
            #    
            #    if key==2:
            #        H1=float(self.lineEdit_2.text())
            #        obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
            #    
            #    obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
            #    obj.size=psuport_data.channel_ss_size
            #    i=self.comboBox_4.currentIndex()
            #    obj.size=psuport_data.channel_ss_size[i] 
            #    ParamS02.S02(obj) 
            #    obj.ViewObject.Proxy=0
                
        elif key==3:#S04
            if key1==0: #アングル
                fname='s04_angle.FCStd'
            elif key1==1:
                fname='s04_channel.FCStd'
            #base=os.path.dirname(os.path.abspath(__file__))
            #joined_path = os.path.join(base, 'pspt_data',fname) 
            #Gui.ActiveDocument.mergeProject(joined_path)
            
            
        elif key==4:#05
            fname='s05_support.FCStd'
            #H1=float(self.lineEdit_L.text())
            #t=float(self.comboBox_5.currentText())
            #d1=float(self.comboBox_4.currentText())
            #obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
            #obj.addProperty("App::PropertyFloat", "t",'Dimension').t=t
            #obj.addProperty("App::PropertyFloat", "d1",'Dimension').d1=d1
            #obj.addProperty("App::PropertyFloat", "b",'Dimension')
            #ParamS05.S05(obj) 
            #obj.ViewObject.Proxy=0
            #FreeCAD.ActiveDocument.recompute() 

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






            #if key==5:
 #
            #    pass
            #elif key==6:
            #    H1=float(self.lineEdit_2.text())
            #L1=float(self.lineEdit_L.text())
            #H=float(self.lineEdit.text())
            #t0=float(self.comboBox_5.currentText())
            #katakou=self.comboBox_3.currentText()
#
            #if self.checkbox.isChecked():
            #    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
            #else:    
            #    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
            #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
#
            #obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
            #obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            #obj.addProperty("App::PropertyFloat", "b",'Dimension')
            #W=float(self.lineEdit_x.text())
            #B=float(self.lineEdit_y.text())    
            #obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            #obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B  
            #if key==6:
            #    obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
            #obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
            #if key1==0:#アングル
            #    label='s07'
            #    obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
            #    obj.size=psuport_data.angle_ss_size
            #    i=self.comboBox_4.currentIndex()
            #    obj.size=psuport_data.angle_ss_size[i] 
            #    ParamS06.S06(obj) 
            #    obj.ViewObject.Proxy=0
            #elif key1==1:
            #    label='s07_C'+size
            #    H0=float(sa[0])
            #    B=float(sa[1])
            #    t1=float(sa[2])
            #    r1=float(sa[4])
            #    r2=float(sa[5])
            #    Cy=float(sa[8])*10
            #    t2=float(sa[3])
            #    obj.addProperty("App::PropertyEnumeration", "size",label)
            #    obj.size=psuport_data.channel_ss_size
            #    i=self.comboBox_4.currentIndex()
            #    obj.size=psuport_data.channel_ss_size[i] 
            #    ParamS06.S06(obj) 
            #    obj.ViewObject.Proxy=0
            
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


            #L1=float(self.lineEdit_L.text())
            #H=float(self.lineEdit.text())
            #if key==8:
            #    H1=float(self.lineEdit_2.text())
#
            #t0=float(self.comboBox_5.currentText())
            #katakou=self.comboBox_3.currentText()
#
            #if self.checkbox.isChecked():
            #    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = True 
            #else:    
            #    obj.addProperty("App::PropertyBool", "BasePlate","BasePlate").BasePlate = False  
            #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
            #obj.addProperty("App::PropertyFloat", "L1",'Dimension').L1=L1
            #obj.addProperty("App::PropertyFloat", "H",'Dimension').H=H
            #obj.addProperty("App::PropertyFloat", "b",'Dimension')
            #if key==8:
            #    obj.addProperty("App::PropertyFloat", "H1",'Dimension').H1=H1
#
            #obj.addProperty("App::PropertyFloat", "t0",'BasePlate').t0=t0
            #W=float(self.lineEdit_x.text())
            #B=float(self.lineEdit_y.text())    
            #obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            #obj.addProperty("App::PropertyFloat", "B",'BasePlate').B=B    
            #if key1==0:#アングル
            #    obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
            #    obj.size=psuport_data.angle_ss_size
            #    i=self.comboBox_4.currentIndex()
            #    obj.size=psuport_data.angle_ss_size[i] 
            #    ParamS08.S08(obj) 
            #    obj.ViewObject.Proxy=0
            #elif key1==1:
            #    obj.addProperty("App::PropertyEnumeration", "size",'Dimension')
            #    obj.size=psuport_data.channel_ss_size
            #    i=self.comboBox_4.currentIndex()
            #    obj.size=psuport_data.channel_ss_size[i] 
            #    ParamS08.S08(obj) 
            #    obj.ViewObject.Proxy=0

        elif key==9:
            fname='s10_support.FCStd'
            #L1=float(self.lineEdit_L.text())
            #H=float(self.lineEdit.text())
            #t=float(self.comboBox_5.currentText())
            #katakou=self.comboBox_3.currentText()
            #obj.addProperty("App::PropertyString", "ShapedSteel",'Type').ShapedSteel=katakou
#
            #obj.addProperty("App::PropertyEnumeration", "Post",'Post')
            #obj.Post=psuport_data.SGP_size
            #i=self.comboBox_4.currentIndex()
            #obj.Post=psuport_data.SGP_size[i]
#
            #obj.addProperty("App::PropertyEnumeration", "TopBeam",'TopBeam')
            #obj.TopBeam=psuport_data.channel_ss_size
            #i=self.comboBox_4.currentIndex()
            #obj.TopBeam=psuport_data.channel_ss_size[i]
            #
            #obj.addProperty("App::PropertyFloat", "L1",'TopBeam').L1=L1
            #obj.addProperty("App::PropertyFloat", "b",'TopBeam')
            #obj.addProperty("App::PropertyFloat", "H",'Post').H=H
            #obj.addProperty("App::PropertyFloat", "t",'BasePlate').t=t
            #W=float(self.lineEdit_x.text())
            #obj.addProperty("App::PropertyFloat", "W",'BasePlate').W=W
            #
            #ParamS10.S10(obj) 
            #obj.ViewObject.Proxy=0
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

 
   
