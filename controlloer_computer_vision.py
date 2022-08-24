from PyQt5 import QtWidgets, QtGui, QtCore
from UI_computer_vision import Ui_MainWindow
import time
import numpy as np
import cv2
import mediapipe as mp   
from app import MainWindow


class MainWindow_controller_computer_vision(QtWidgets.QMainWindow):
    returnSignal = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.timer_camera = QtCore.QTimer()
        self.timer_camera2 = QtCore.QTimer()
        self.timer_camera3 = QtCore.QTimer()
        self.timer_camera4 = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.ui.setupUi(self)
        self.setup_control()
        



#--------------------------------------Control-----------------------------------------
    def setup_control(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.ui.pushButton.clicked.connect(self.slotcamera)
        self.timer_camera3.timeout.connect(self.show_camera3)
        #self.ui.pushButton_3.clicked.connect(self.blazeposecamera)
        self.ui.pushButton_2.clicked.connect(self.show_segmentation)
        self.timer_camera2.timeout.connect(self.show_camera2)
        self.ui.pushButton_3.clicked.connect(self.blazeposecamera)
        #self.ui.pushButton_3.clicked.connect(self.show_camera3)

        #self.timer_camera2.timeout.connect(self.show_camera2)
        #self.ui.pushButton_3.clicked.connect(self.openposecamera)
        self.timer_camera4.timeout.connect(self.show_camera4)
        self.ui.pushButton_4.clicked.connect(self.opentrackercamera)
        self.ui.pushButton.setText('打開攝像頭')
        

#---------------------------------------------------------------------------------------

    # 一號原始鏡頭

    def slotcamera(self):
        if self.timer_camera.isActive() == False:
            self.opencamera()
        else:
            self.closeCamera()



    def show_camera(self):

        flag,self.image = self.cap.read()
        show = cv2.resize(self.image,(660,590))
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))


    

    def opencamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.Warning(self,u'Warning',u'請檢查設備',buttons = QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(30)
            self.ui.pushButton.setText('關閉攝像頭')

    def closeCamera(self):
        self.timer_camera.stop()
        self.cap.release()
        self.ui.label.clear()
        self.ui.pushButton.setText('打開攝像頭')

#------------------------------------------------------------------------------------------------------------------
    #yolo camera
    def show_camera3(self):
        
        # showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888)
        # self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        myDraw = mp.solutions.drawing_utils
        myPose = mp.solutions.pose
        pose = myPose.Pose()
        pTime = 0

        success , self.img = self.cap.read()
        show = cv2.resize(self.img,(660,590))
        show = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        results = pose.process(show)
    # print(results.pose_landmarks)
        if results.pose_landmarks:
            myDraw.draw_landmarks(self.img, results.pose_landmarks, myPose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = self.img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(self.img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(self.img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", self.img)

    #cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
            self.cap.release()
        # showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888)
        # self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))



    def blazeposecamera(self):
        if self.timer_camera.isActive() == False:
            self.blazeposeposecamera()
        else:
            self.closeblazeposeposeCamera()


#---------------------------------------------------------------------------------------
    def show_segmentation(self):
        self.ui = MainWindow()
        self.ui.show()



    def blazeposeposecamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.Warning(self,u'Warning',u'請檢查設備',buttons = QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera3.start(30)
            self.ui.pushButton.setText('關閉攝像頭')

    def closeblazeposeposeCamera(self):
        self.timer_camera3.stop()
        self.cap.release()
        self.ui.label.clear()
        self.ui.pushButton.setText('打開攝像頭')



    #openpose camera   二號鏡頭

    def show_camera2(self):
        
        mpHands = mp.solutions.hands
        
        hands = mpHands.Hands()
        myDraw = mp.solutions.drawing_utils
    
        handLmsStyle = myDraw.DrawingSpec(color=(0,0,255),thickness=5)
        handConStyle = myDraw.DrawingSpec(color=(0,255,0),thickness=5)
        flag,self.image = self.cap.read()
        show = cv2.resize(self.image,(660,590))
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB)
        result = hands.process(show)
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                myDraw.draw_landmarks(show,handLms,mpHands.HAND_CONNECTIONS,handLmsStyle,handConStyle)
                
            
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))



    def openposecamera(self):
        if self.timer_camera2.isActive() == False:
            self.openposeopencamera()
        else:
            self.closeposeCamera()

    def openposeopencamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.Warning(self,u'Warning',u'請檢查設備',buttons = QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera2.start(30)
            self.ui.pushButton.setText('關閉攝像頭')

    def closeposeCamera(self):
        self.timer_camera2.stop()
        self.cap.release()
        self.ui.label.clear()
        self.ui.pushButton.setText('打開攝像頭')



    ## 追蹤模式的鏡頭
    def show_camera4(self):
        import sys

        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
         
        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        tracker_type = tracker_types[7]  #設定追蹤器的類型
        
        if int(minor_ver) < 3:
            tracker = cv2.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
            if tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
            if tracker_type == "CSRT":
                tracker = cv2.TrackerCSRT_create()

        #flag,self.image = self.cap.read()
        if not self.cap.isOpened():
            print("Could not open video")
            sys.exit()
        ok,self.image = self.cap.read()
        if not ok:
            print ('Cannot read video file')
            sys.exit()
        self.bbox = (287, 23, 86, 320)
        self.bbox = cv2.selectROI(self.image, False)
        showImage = QtGui.QImage(self.image.data,self.image.shape[1],self.image.shape[0],QtGui.QImage.Format_RGB888)
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        ok = tracker.init(self.image, self.bbox)

        while True:
            ok,self.image = self.cap.read()
            if not ok:
                break
            timer = cv2.getTickCount()
            ok,self.bbox = tracker.update(self.image)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            if ok:
                p1 = (int(self.bbox[0]), int(self.bbox[1]))
                p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
                self.image = cv2.rectangle(self.image, p1, p2, (255,0,0), 2, 1)
                self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
                self.image = cv2.putText(self.image, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
                self.image = cv2.putText(self.image, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
                showImage = QtGui.QImage(self.image.data,self.image.shape[1],self.image.shape[0],QtGui.QImage.Format_RGB888)
                self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
                # if self.ui.pushButton_4.clicked.connect(self.closetrackerCamera):
                #     break
            else:
                self.image = cv2.putText(self.image, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                self.image = cv2.putText(self.image, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
                self.image = cv2.putText(self.image, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
            k = cv2.waitKey(1) & 0xff
            if k == ord('q') : 
                break
            self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(self.image.data,self.image.shape[1],self.image.shape[0],QtGui.QImage.Format_RGB888)
            self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))

        

    
    def opentrackercamera(self):
        if self.timer_camera4.isActive() == False:
            self.opentrackertracekercamera()
        else:
            self.closetrackerCamera()
    def opentrackertracekercamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.Warning(self,u'Warning',u'請檢查設備',buttons = QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera4.start(30)
            self.ui.pushButton.setText('關閉攝像頭')
    def closetrackerCamera(self):
        self.timer_camera4.stop()
        self.cap.release()
        self.ui.label.clear()
        self.ui.pushButton.setText('打開攝像頭')




    
