from PyQt5 import QtWidgets
from controller_LCC import MainWindow_controller_LCC


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller_LCC()
    window.show()
    sys.exit(app.exec_())