from PyQt5 import QtWidgets
from controller_check import MainWindow_controller_check



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller_check()
    window.show()
    sys.exit(app.exec_())