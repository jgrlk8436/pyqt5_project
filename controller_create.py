from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
from create import Ui_MainWindow
import re
import controller_check
from trycode.secret import enctry

class MainWindow_controller_create(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_c()
        self.db_name = 'login.sqlite'
        self.window_check = controller_check.MainWindow_controller_check()
        #self.execute_db()
        

    #定義連結資料庫
    def execute_db(self,cmd):
        self.cmd = cmd
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(self.cmd)
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
        self.ui.pushButton.clicked.connect(self.buttonClicked)
        self.ui.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ui.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        #self.ui.secret_lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)


    def buttonClicked(self):
        #print('aaaa')
        import random
        self.user = str(self.ui.lineEdit.text())
        self.account = str(self.ui.lineEdit_2.text()) 
        self.email_ = str(self.ui.lineEdit_3.text())
        self.pass_ = str(self.ui.lineEdit_4.text())
        self.repass = str(self.ui.lineEdit_5.text())
        self.newpass_ = enctry(self.pass_)
        self.newrepass = enctry(self.repass)
        self.randnum = random.randint(1000,9999)
        cmd = 'INSERT INTO login(姓名,帳號,信箱,密碼,確認密碼,checkint,隨機碼) VALUES("%s","%s","%s","%s","%s","%d","%d")' %(self.user,self.account,self.email_,self.newpass_,self.newrepass,int(0),int(self.randnum))
        rex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        
        
        if (self.ui.lineEdit.text() != None) and (self.ui.lineEdit_2.text() != None) and (self.ui.lineEdit_3.text() != None) and (self.ui.lineEdit_4.text() != None) and (self.ui.lineEdit_5.text() != None):
            #QtWidgets.QMessageBox.warning(self,'注意','任一欄位不能為空!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
            if re.match(rex,self.email_) == None:
                QtWidgets.QMessageBox.warning(self,'注意','信箱格式不對!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
            else:    
                if self.pass_ != self.repass:
                    QtWidgets.QMessageBox.warning(self,'注意','確認密碼不正確!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
                else:
                    self.execute_db(cmd)
                    self.smtp()
                    QtWidgets.QMessageBox.warning(self,'注意','~帳號申請完成~請至信箱完成開通!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit_2.clear()
                    self.ui.lineEdit_3.clear()
                    self.ui.lineEdit_4.clear()
                    self.ui.lineEdit_5.clear()
                    self.window_check.show()
        else:
            QtWidgets.QMessageBox.warning(self,'注意','任一欄位不能為空!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)

        # 帳號 self.ui.account_lineEdit.text() 密碼 self.ui.secret_lineEdit.text()


    def smtp(self):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        self.email_ = str(self.ui.lineEdit_3.text())
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] = "Welcome to HAOHAO SYSTEM!!"  #郵件標題
        content["from"] = "jgrlk8444@gmail.com"  #寄件者
        content["to"] = f"{self.email_}" #收件者
        content.attach(MIMEText(f"This is your key. The number is {self.randnum}\n"))  #郵件內容
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("jgrlk8444@gmail.com", "fpeyjqfphgibuipj")  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                #print("Complete!")
            except Exception as e:
                print("Error message: ", e)