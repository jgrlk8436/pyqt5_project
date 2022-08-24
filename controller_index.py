
from PyQt5 import QtWidgets, QtGui, QtCore
from controller_data_analysis import MainWindow_controller_data_analysis
from controlloer_computer_vision import MainWindow_controller_computer_vision
from controller_LCC import MainWindow_controller_LCC
from controller_picture import MainWindow_controller_picture
import index
import analysis
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
import sqlite3
import os
class MainWindow_controller_index(QtWidgets.QMainWindow):

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # self.db_path = os.path.join(BASE_DIR,"login.sqlite")

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = index.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_c()
        self.initDBConnection()
        self.data_analysis = MainWindow_controller_data_analysis()
        self.computer_vision = MainWindow_controller_computer_vision()
        self.web_crawler = MainWindow_controller_LCC()
        self.picture = MainWindow_controller_picture()
        self.browser = QWebEngineView()
        # self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # self.db_path = os.path.join(self.BASE_DIR,"login.sqlite")
        



    def initDBConnection(self):
        self.dbConnection = sqlite3.connect("login.sqlite")


    def setup_c(self):
        self.clicked_counter = 0
        self.ui.Data_Analysis_btn.clicked.connect(self.data_analysisClicked)
        self.ui.webcam_detect_btn.clicked.connect(self.computer_visionClicked)
        self.ui.Web_Crawler_btn.clicked.connect(self.LCC)
        self.ui.yolo_btn.clicked.connect(self.web)
        self.ui.Computer_Vision_btn.clicked.connect(self.picturedetect)
        self.ui.pushButton.clicked.connect(self.showTableData)
        


    def data_analysisClicked(self):
        self.data_analysis.show()
        #self.ui.label.setText(self.ui.lineEdit.text())
    def computer_visionClicked(self):
        self.computer_vision.show()

    def LCC(self):
        QtWidgets.QMessageBox.warning(self,'注意','牽涉到隱私，此功能不開放~~^_^',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
        self.web_crawler.show()


    def web(self):
        self.browser.load(QtCore.QUrl("https://share.streamlit.io/jgrlk8436/main/main/index.py"))
        self.browser.show()
        
    def picturedetect(self):
        self.picture.show()

    def showTableData(self):
        result = self.dbConnection.cursor().execute("""SELECT * FROM login""")
        for row_number,row_data in enumerate(result):
            self.ui.tableWidget.insertRow(row_number)
            for column_number,column_data in enumerate(row_data):
                item = str(column_data);
                # if(column_number != 0):
                self.ui.tableWidget.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(item))