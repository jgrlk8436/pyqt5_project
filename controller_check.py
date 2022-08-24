from PyQt5 import QtWidgets, QtGui, QtCore
import check
import sqlite3
class MainWindow_controller_check(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = check.Ui_MainWindow()
        self.db_name = 'login.sqlite'
        self.ui.setupUi(self)
        self.setup_c()
        

    def setup_c(self):
        self.clicked_counter = 0
        self.ui.pushButton.clicked.connect(self.check_Clicked)
        
    #定義連結資料庫
    def execute_db(self,cmd):
        self.cmd = cmd
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(self.cmd)
        conn.commit()
        conn.close()

    def check_Clicked(self):
        conn=sqlite3.connect(self.db_name)
        cursor=conn.cursor()
        cmd = 'SELECT * FROM login ORDER BY id DESC LIMIT 1 '
        cursor.execute(cmd)
        result = cursor.fetchall()
        newid = ''
        numb = ''
        for item in result:
            newid += str(item[0])
            numb += str(item[7])
        if self.ui.lineEdit.text() == None:
            QtWidgets.QMessageBox.warning(self,'注意','欄位不能為空!!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            if str(numb) == str(self.ui.lineEdit.text()):
                cmd2 = f'UPDATE login SET checkint = 1 WHERE id="{newid}"'
                self.execute_db(cmd2)
                QtWidgets.QMessageBox.warning(self,'注意','恭喜，帳號完成開通!!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
            else:
                QtWidgets.QMessageBox.warning(self,'注意','驗證碼驗證失敗，請重新輸入',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)