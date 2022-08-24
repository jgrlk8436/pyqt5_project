from PyQt5 import QtWidgets, QtGui, QtCore
from analysis import Ui_MainWindow
import requests
import time
import matplotlib.pyplot as plt


class MainWindow_controller_data_analysis(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_c()
        
    def setup_c(self):
        self.clicked_counter = 0
        self.ui.pushButton.clicked.connect(self.buttonClicked)


    def buttonClicked(self):
        player = self.ui.lineEdit.text()
        if player == '':
            QtWidgets.QMessageBox.warning(self,'注意','欄位不能為空!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
        else:
            try:
                self.search(player)
            except:
                QtWidgets.QMessageBox.warning(self,'注意','查無此球員!!',QtWidgets.QMessageBox.StandardButton.Ok ,QtWidgets.QMessageBox.StandardButton.Ok)
        



    #定義函數 抓取球員的資料      
    def catchplayer(self,a):
        self.a = a
        
        try:
            global peopledata
            # a = str(input("請輸入球員名稱:"))
            url = 'https://tw.global.nba.com/stats2/player/stats.json?ds=profile&locale=zh_TW&playerCode='+ self.a
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
            response = requests.get(url, headers=headers)
            peopledata = response.json()
            return peopledata
        except:
            QtWidgets.QMessageBox.warning(self,'注意','查無此球員!!',QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,QtWidgets.QMessageBox.StandardButton.Yes)
            time.sleep(10)
 


    def search(self,player):
        self.player = player
        self.player = self.player.lower()
        #print(self.player)
        self.string1 = self.player.split()[0]
        self.string2 = self.player.split()[1]
        self.output = self.string1 + '_' + self.string2
        self.catchplayer(self.output)
        # print('場均上場時間:',peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["minsPg"])
        # print('本賽季目前:')
        # print('場均得分:',peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["pointsPg"])
        # print('場均助攻:',peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["assistsPg"])
        # print('場均籃板:',peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["defRebsPg"])
        # print('場均阻攻:',peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["blocksPg"])
        # print('場均抄截:',peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["stealsPg"])    
        self.playerlist=''
        self.playerlist += '本賽季目前統計:'+'\n'
        self.playerlist += '場均上場時間:'+str(peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["minsPg"])+'\n'
        self.playerlist += '場均得分:'+str(peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["pointsPg"])+'\n'
        self.playerlist += '場均助攻:'+str(peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["assistsPg"])+'\n'
        self.playerlist += '場均籃板:'+str(peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["defRebsPg"])+'\n'
        self.playerlist += '場均阻攻:'+str(peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["blocksPg"])+'\n'
        self.playerlist += '場均抄截:'+str(peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["stealsPg"])+'\n'

        self.ui.player_label.setText(self.playerlist)

        y = [peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["minsPg"],
             peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["pointsPg"],
             peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["assistsPg"],
             peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["defRebsPg"],
             peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["blocksPg"],
             peopledata["payload"]["player"]["stats"]["currentSeasonTypeStat"]["currentSeasonTypePlayerTeamStats"][0]["statAverage"]["stealsPg"]
             ]
        x = ["Time","Point","Assist","Rebound","Block","Steal"]
        B = self.output.split("_",2)
        C = B[0].title()+" "+B[1].title()
        plt.figure(figsize=(6,4),facecolor="lightblue")
        picture1=plt.bar(x,y, width=0.5 ,color=['red','orange','yellow','green','blue','purple'])
            
        for a1,b1 in zip(x,y):
            plt.text(a1, b1+0.5, '%.2f' % b1, ha='center', va= 'bottom',fontsize=10)
        plt.ylim(0,40)
        plt.xlabel("2021-2022")
        plt.ylabel("Average")
        plt.title(C+" data")
        #plt.figure(1)
        plt.show()

    
        self.history=''
        self.history += '歷史數據統計:'+'\n'
        self.history += '平均上場時間:'+str(peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["mins"])+'\n'
        self.history += '場均得分:'+str(peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["points"])+'\n'
        self.history += '場均助攻:'+str(peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["assists"])+'\n'
        self.history += '場均籃板:'+str(peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["defRebs"])+'\n'
        self.history += '場均阻攻:'+str(peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["blocks"])+'\n'
        self.history += '場均抄截:'+str(peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["steals"])+'\n'

        self.ui.history_label.setText(self.history)

        y1=[peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["mins"],
             peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["points"],
             peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["assists"],
             peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["defRebs"],
             peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["blocks"],
             peopledata["payload"]["player"]["stats"]["regularSeasonCareerStat"]["statTotal"]["steals"]
             ]
        x = ["Time","Point","Assist","Rebound","Block","Steal"]
        plt.figure(figsize=(6,4),facecolor="lightblue")
        self.picture2=plt.bar(x,y1, width=0.5 ,color=['red','orange','yellow','green','blue','purple'])
        #在長條圖上方加上數值
        for a1,b1 in zip(x,y1):
            plt.text(a1, b1+0.5, '%.2f' % b1, ha='center', va= 'bottom',fontsize=10) 
        plt.xlabel("career-totals")    
        plt.title(C+" data")
        #plt.figure(2)
        plt.show()
