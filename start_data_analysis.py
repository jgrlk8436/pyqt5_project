from PyQt5 import QtWidgets
from controller_data_analysis import MainWindow_controller_data_analysis


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller_data_analysis()
    window.show()
    sys.exit(app.exec_())