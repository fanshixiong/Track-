# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'te.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import cv2
import sys
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = MyLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 49, 601, 288))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
from mylabel import MyLabel


class Example(QWidget):
    def __init__(self):
        super().__init__()
        i=5
        while (i < 100 ):
            self.initUI()
            ++i
    def initUI(self):
        self.resize(675, 300)
        self.setWindowTitle('在label中绘制矩形')
        self.lb = MyLabel(self)  #重定义的label
        self.lb.setGeometry(QRect(30, 30, 511, 541))
        img = cv2.imread('back2.jpg')
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine,QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.lb.setPixmap(pixmap)
        self.lb.setCursor(Qt.CrossCursor)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = Example()
    sys.exit(app.exec_())