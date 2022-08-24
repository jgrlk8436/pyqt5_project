from PyQt5 import QtWidgets
from controller_create import MainWindow_controller_create
import controller_create
import sqlite3
from login import Ui_MainWindow
#from controller_index import MainWindow_controller_index
from controller_login import MainWindow_controller_login

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller_login()
    window2 = controller_create.MainWindow_controller_create()
    window.show()
    window2.hide()
    window.ui.create_btn.clicked.connect(window2.show)
    sys.exit(app.exec_())
    