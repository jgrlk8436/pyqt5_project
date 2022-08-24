from PyQt5 import QtWidgets
from controller_index import MainWindow_controller_index
from controller_data_analysis import MainWindow_controller_data_analysis

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller_index()
    window2 = MainWindow_controller_data_analysis()
    window.show()
    #window.ui.Data_Analysis_btn.clicked.connect(window2.show)
    #window.show()
    sys.exit(app.exec_())