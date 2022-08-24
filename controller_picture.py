from turtle import shape
from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
from PyQt5.QtWidgets import QFileDialog
from Picture import Ui_MainWindow
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtWidgets,QtGui,QtCore
import numpy as np
import  matplotlib.pyplot as plt 
class MainWindow_controller_picture(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_c()
        

    def setup_c(self):
        self.ui.pushButton.clicked.connect(self.open_file)
        #self.display_img(self.filename)
        self.ui.pushButton_2.clicked.connect(self.invert)
        self.ui.pushButton_3.clicked.connect(self.darken)
        self.ui.pushButton_4.clicked.connect(self.lighten)
        self.ui.pushButton_5.clicked.connect(self.gaussian)
        self.ui.pushButton_6.clicked.connect(self.canny)
        

    def open_file(self):
        self.filename, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
            "Open file",
            "./")
        #print(filename,filetype)
        #self.ui.label.setText(self.filename)
        self.display_img(self.filename)
    
    def display_img(self,filename):
        self.filename = filename
        self.img = cv2.imread(self.filename)
        height,width,channel = self.img.shape
        bytesPerline = 3*width
        self.qimg = QImage(self.img,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
        self.ui.label.setPixmap(QPixmap.fromImage(self.qimg))
        self.ui.label.adjustSize()

    def invert(self):
        self.img = cv2.imread(self.filename)
        self.res = 255-self.img
        height,width,channel = self.res.shape
        bytesPerline = 3*width
        self.qimg = QImage(self.res,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
        self.ui.label_2.setPixmap(QPixmap.fromImage(self.qimg))
        self.ui.label.adjustSize()
        
    
    def darken(self):
        self.img = cv2.imread(self.filename)
        self.img[self.img<128]=128
        self.res = self.img-128
        height,width,channel = self.res.shape
        bytesPerline = 3*width
        self.qimg = QImage(self.res,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
        self.ui.label_2.setPixmap(QPixmap.fromImage(self.qimg))
        self.ui.label.adjustSize()


    def lighten(self):
        self.img = cv2.imread(self.filename)
        self.res = np.clip(self.img*2,0,255)
        height,width,channel = self.res.shape
        bytesPerline = 3*width
        self.qimg = QImage(self.res,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
        self.ui.label_2.setPixmap(QPixmap.fromImage(self.qimg))
        self.ui.label.adjustSize()

    def gaussian(self):
        self.img=  cv2.imread(self.filename)
        self.img = cv2.GaussianBlur(self.img,(7,7),0)
        height,width,channel = self.img.shape
        bytesPerline = 3*width
        self.qimg = QImage(self.img,width,height,bytesPerline,QImage.Format_RGB888).rgbSwapped()
        self.ui.label_2.setPixmap(QPixmap.fromImage(self.qimg))
        self.ui.label.adjustSize()

    
    def canny(self):
        self.img=  cv2.imread(self.filename)
        gaussian = cv2.GaussianBlur(self.img,(5,5),0)
        self.edges = cv2.Canny(gaussian,100,200)
        cv2.imshow("canny edge detection",self.edges)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()


    
        
        





    

    