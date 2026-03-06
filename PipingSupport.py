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
        Dialog.resize(365, 220)
        Dialog.move(800, 0)
        #形式
        self.label = QtGui.QLabel('Type',Dialog)
        self.label.setGeometry(QtCore.QRect(10, 0, 81, 20))
        self.label.setStyleSheet("color: gray;")
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(100, 0, 100, 20))
        self.comboBox.setObjectName("comboBox")
        #形鋼
        self.label_3 = QtGui.QLabel('ShapedSteel',Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 25, 81, 20))
        self.label_3.setStyleSheet("color: black;")
        self.comboBox_3 = QtGui.QComboBox(Dialog)
        self.comboBox_3.setGeometry(QtCore.QRect(100, 26, 100, 20))
        self.comboBox_3.setMaxVisibleItems(10)
        self.comboBox_3.setObjectName("comboBox_3")
        #サイズ
        self.label_size = QtGui.QLabel('Size',Dialog)
        self.label_size.setGeometry(QtCore.QRect(10, 50, 81, 20))
        self.label_size.setStyleSheet("color: black;")
        self.comboBox_size = QtGui.QComboBox(Dialog)
        self.comboBox_size.setGeometry(QtCore.QRect(100, 52, 100, 20))
        self.comboBox_size.setMaxVisibleItems(10)
        self.comboBox_size.setObjectName("comboBox_3")
        #H
        self.label_H = QtGui.QLabel('H',Dialog)
        self.label_H.setGeometry(QtCore.QRect(10, 80, 81, 20))
        self.label_H.setStyleSheet("color: black;")
        self.le_H = QtGui.QLineEdit('500',Dialog)
        self.le_H.setGeometry(QtCore.QRect(100, 80, 100, 20))
        self.le_H.setAlignment(QtCore.Qt.AlignCenter)
        #L
        self.label_L = QtGui.QLabel('L',Dialog)
        self.label_L.setGeometry(QtCore.QRect(10, 100, 81, 20))
        self.label_L.setStyleSheet("color: black;")
        self.le_L = QtGui.QLineEdit('500',Dialog)
        self.le_L.setGeometry(QtCore.QRect(100, 103, 100, 20))
        self.le_L.setAlignment(QtCore.Qt.AlignCenter)
        #H1
        self.label_h1 = QtGui.QLabel('H1',Dialog)
        self.label_h1.setGeometry(QtCore.QRect(10, 125, 81, 20))
        self.label_h1.setStyleSheet("color: black;")
        self.le_h1 = QtGui.QLineEdit('250',Dialog)
        self.le_h1.setGeometry(QtCore.QRect(100, 128, 100, 20))
        self.le_h1.setAlignment(QtCore.Qt.AlignCenter)
        #図形
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(220, 0, 130, 110))
        self.label_7.setText("")
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)

        #実行      
        self.pushButton = QtGui.QPushButton('Create',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 160, 70, 20))
        self.pushButton.setObjectName("pushButton")
        #update
        self.pushButton2 = QtGui.QPushButton('Update',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(110, 160, 80, 20))
        #import
        self.pushButton3 = QtGui.QPushButton('Import data',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(10, 185, 190, 20))

        self.comboBox.addItems(psuport_data.type)
        self.comboBox_3.addItems(psuport_data.katakou)
        self.comboBox.setCurrentIndex(1)
        self.comboBox.currentIndexChanged[int].connect(self.onType)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(1)
        self.comboBox_3.currentIndexChanged[int].connect(self.onKatakou)
        self.comboBox_3.setCurrentIndex(0)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.Import)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.onUpdate)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.onUpdate)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def Import(self):
         global spreadsheet
         global channel
         global angle
         global s10
         selection = Gui.Selection.getSelection()
         if selection:
             selected_object = selection[0]
             if selected_object.TypeId == "App::Part":
                 parts_group = selected_object
                 for obj in parts_group.Group:
                    #print(obj.Label)
                    if obj.TypeId == "Spreadsheet::Sheet":
                        spreadsheet = obj
                    elif obj.Label=='ChannelSteel':
                        channel=obj    
                    elif obj.Label=='AngleSteel':
                        angle=obj 
                    elif obj.Label=='s10':
                        s10=obj    
                 self.comboBox.setCurrentText(spreadsheet.getContents('type'))   
                 self.le_H.setText(spreadsheet.getContents('H0'))
                 try:
                     self.le_L.setText(spreadsheet.getContents('L0'))
                 except:
                     pass
                 try:
                     self.le_h1.setText(spreadsheet.getContents('h1'))
                 except:
                     pass
                 myKey=self.comboBox_3.currentText()
                 #print(key1)
                 if myKey=='Angle':
                     size=angle.size
                 elif myKey=='Channel':
                     size=channel.size
                 elif myKey=='Post':
                     size=s10.Post   
                 elif myKey=='Capping':
                     size=s10.TopBeam     
                 try:      
                     self.comboBox_size.setCurrentText(size)
                 except:
                     pass

    def onUpdate(self):
        H=self.le_H.text()
        L=self.le_L.text()
        try:
            h1=self.le_h1.text()
        except:
            pass

        myKey=self.comboBox_3.currentText()
        if myKey=='Channel':
            channel.size=self.comboBox_size.currentText()
            bW=channel.B
            bH=channel.H
            spreadsheet.set('bW',str(bW))
            spreadsheet.set('bH',str(bH))
        elif myKey=='Capping':
            s10.TopBeam =self.comboBox_size.currentText()   
        elif myKey  =='Post':
            s10.Post=self.comboBox_size.currentText()  
        elif myKey=='Angle':
            angle.size=self.comboBox_size.currentText() 
             
        spreadsheet.set('H0',H)
        try:
            spreadsheet.set('L0',L)
        except:
            pass
        try:
            spreadsheet.set('h1',h1)
        except:
            pass
        App.ActiveDocument.recompute()    
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
        #if key==9:
        #    self.comboBox_5.setCurrentIndex(3)
        pic=img + '.jpg'
        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, "pspt_data",pic)
        self.label_7.setPixmap(QtGui.QPixmap(joined_path))
    def onKatakou(self):
        global key1
        global katakou_size
        self.comboBox_size.clear()
        key1=self.comboBox_3.currentIndex()
        #print(key)
        if key<=8:
            if key==4:
                katakou_size=psuport_data.RB_ss_size
                self.comboBox_size.addItems(katakou_size)
            else:
                if key1==0:
                    katakou_size=psuport_data.angle_ss_size
                    self.comboBox_size.addItems(katakou_size)
                elif key1==1:
                    katakou_size=psuport_data.channel_ss_size
                    self.comboBox_size.addItems(katakou_size)
        elif key==9:
            if key1==0:#支柱
                katakou_size=psuport_data.SGP_size
            elif key1==1:#笠木
                katakou_size=psuport_data.channel_ss_size
            self.comboBox_size.addItems(katakou_size)

    def create(self):
        doc = App.ActiveDocument
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
            #Gui.ActiveDocument.mergeProject(joined_path) 
        except:
            pass 
        
        # --- インポート前のオブジェクトリストを取得 ---
        old_obj_names = [o.Name for o in doc.Objects]
        
        # マージ実行
        Gui.ActiveDocument.mergeProject(joined_path)
        doc.recompute() # 一旦再計算して内部IDを確定させる
    
        # --- インポート後に増えたオブジェクトを特定 ---
        new_objs = [o for o in doc.Objects if o.Name not in old_obj_names]
        
        if not new_objs:
            print("Error: オブジェクトが読み込まれませんでした。")
            return
    
        # trstleAssyというラベルを持つものを優先的に探す
        move_target = None
        for o in new_objs:
            if "supportAssy" in o.Label or "supportAssy" in o.Name:
                move_target = o
                break
        
        # 見つからなければ、新しく入ってきた最初のオブジェクトをターゲットにする
        if not move_target:
            move_target = new_objs[0]
    
        view = Gui.ActiveDocument.ActiveView
        callbacks = {}
    
        def move_cb(info):
            pos = info["Position"]
            # 重要：ビュー平面上の3D座標を取得
            p = view.getPoint(pos)
            if move_target:
                move_target.Placement.Base = p
                #view.softRedraw()
    
        def click_cb(info):
            if info["State"] == "DOWN" and info["Button"] == "BUTTON1":
                # コールバック解除
                view.removeEventCallback("SoLocation2Event", callbacks["move"])
                view.removeEventCallback("SoMouseButtonEvent", callbacks["click"])
                App.ActiveDocument.recompute()
                print("Placed: " + move_target.Label)
    
        # イベント登録
        callbacks["move"] = view.addEventCallback("SoLocation2Event", move_cb)
        callbacks["click"] = view.addEventCallback("SoMouseButtonEvent", click_cb)
        #doc = App.ActiveDocument
#
        #last_part = next((obj for obj in reversed(doc.Objects) if obj.TypeId == "App::Part"), None)
        #if last_part:
        #     Gui.Selection.clearSelection()
        #     Gui.Selection.addSelection(doc.Name, last_part.Name)
        #else:
        #    pass
        #
        #Gui.activateWorkbench("DraftWorkbench")
        #Gui.Selection.addSelection(last_part)
        #Gui.runCommand('Draft_Move',0) 

class main():
        w = QtGui.QWidget()
        w.ui = Ui_Dialog()
        w.ui.setupUi(w)
        w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        w.show()

 
   
