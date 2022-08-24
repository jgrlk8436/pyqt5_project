from PyQt5 import QtWidgets
from controlloer_computer_vision import MainWindow_controller_computer_vision


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller_computer_vision()
    window.show()
    sys.exit(app.exec_())