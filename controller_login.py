from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

import cv2
from login import Ui_MainWindow
from controller_index import MainWindow_controller_index


class MainWindow_controller_login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.db_name = 'login.sqlite'
        self.ui.setupUi(self)
        self.setup_c()
        self.index = MainWindow_controller_index()
        
        

    #定義連結資料庫
    def execute_db(fname,sql_cmd):
        conn = sqlite3.connect(fname)
        c = conn.cursor()
        c.execute(sql_cmd)
        conn.commit()
        conn.close()


    # 加密
    def enctry(self,s):
        self.s = s
        k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
        self.encry_str = ""
        for i,j in zip(self.s,k):
            # i為字元，j為祕鑰字元
            temp = str(ord(i)+ord(j))+'_' # 加密字元 = 字元的Unicode碼 + 祕鑰的Unicode碼
            self.encry_str = self.encry_str + temp
        return self.encry_str

    # 解密
    def dectry(self,p):
        self.p = p
        k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
        self.dec_str = ""
        for i,j in zip(self.p.split("_")[:-1],k):
            # i 為加密字元，j為祕鑰字元
            temp = chr(int(i) - ord(j)) # 解密字元 = (加密Unicode碼字元 - 祕鑰字元的Unicode碼)的單位元組字元
            self.dec_str = self.dec_str+temp
        return self.dec_str



    def setup_c(self):
        self.ui.create_btn.clicked.connect(self.buttonClicked)
        self.ui.secret_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ui.login_btn.clicked.connect(self.loginclicked)
        self.img_path = '999.png'
        self.display_img()
    
    def display_img(self):
        self.img = cv2.imread(self.img_path)
        height,width,channed = self.img.shape
        bytesPerline = 3 * width
        self.qimg = QtGui.QImage(self.img,width,height,bytesPerline,QtGui.QImage.Format_RGB888).rgbSwapped()
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(self.qimg))
        
    def loginclicked(self):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        cmd = f'select * from login where 帳號="{self.ui.account_lineEdit.text()}" '
        cursor.execute(cmd)
        result = cursor.fetchall()
        account=''
        passw=''
        checkcheck = ''
        for item in result:
            account+=item[2]
            passw += self.dectry(item[4])
            checkcheck += str(item[6])
        print(checkcheck)
        
        if (self.ui.account_lineEdit.text() == account) and (self.ui.secret_lineEdit.text()==passw) :
            if checkcheck =='1':

                print('登入成功')
                self.index.show()
            else:
                QtWidgets.QMessageBox.warning(self,'注意','此帳號驗證失敗!!請重新申請!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            QtWidgets.QMessageBox.warning(self,'注意','登入失敗!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
    
        
    def buttonClicked(self):
        print(f'{self.ui.secret_lineEdit.text()}')
        
