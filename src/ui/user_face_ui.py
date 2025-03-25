# ui/user_face_ui.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
import cv2
from utils.face_utils import detect_faces
from utils.constants import NAMES

class Ui_face_reco(QWidget):
    def __init__(self):
        super(Ui_face_reco, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        # 加载训练好的数据
        self.recognizer.read('./data/Face_training/trainer.yml')
        self.cascadePath = "./resources/haarcascades/haarcascade_frontalface_default.xml"
        self.faceCascade4 = cv2.CascadeClassifier(self.cascadePath)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.init_ui()
        self.camera_init()
        self.face_rec()

    def init_ui(self):
        self.resize(1280, 800)
        self.lab_face = QLabel(self)
        self.lab_face.setGeometry(15, 40, 960, 720)
        self.lab_face.setFrameShape(QtWidgets.QFrame.Box)
        self.btn_back = QPushButton("返回", self)
        self.btn_back.setGeometry(1090, 670, 81, 51)
        self.btn_back.setStyleSheet("font: 75 16pt;")
        self.btn_back.clicked.connect(self.slot_btn_back)

    def camera_init(self):
        self.CAM_NUM = 0
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)

    def face_rec(self):
        if not self.timer_camera.isActive():
            flag = self.cap.open(self.CAM_NUM)
            if not flag:
                QtWidgets.QMessageBox.warning(self, "Warning", "请检测相机与电脑是否连接正确", QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(10)
        else:
            self.timer_camera.stop()
            self.cap.release()

    def show_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, -1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade4.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(0.1*self.cap.get(3)), int(0.1*self.cap.get(4)))
            )
            try:
                if not any(faces):
                    # 当没有检测到人脸时，可添加控制逻辑（例如：GPIO 控制门锁）  
                    pass
            except Exception as e:
                print(e)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                if confidence < 90:
                    id = NAMES[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                    # 此处可以调用门禁开锁函数
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                    # 此处可以调用门禁关锁函数
                cv2.putText(frame, str(id), (x+5, y-5), self.font, 1, (255,255,255), 2)
                cv2.putText(frame, str(confidence), (x+5, y+h-5), self.font, 1, (255,255,0), 1)
            show = cv2.resize(frame, (960,720))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.lab_face.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def slot_btn_back(self):
        from ui.menu_ui import Ui_Menu
        self.menu = Ui_Menu()
        self.menu.show()
        self.timer_camera.stop()
        self.cap.release()
        self.hide()
