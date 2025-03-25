# ui/user_face_ui.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
import cv2, numpy as np
from picamera2 import Picamera2
from utils.face_utils import detect_faces
from utils.constants import NAMES
import time


class Ui_face_reco(QWidget):
    def __init__(self):
        super(Ui_face_reco, self).__init__()
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": (640,480)})
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(1)
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)
        self.init_ui()
        self.camera_init()
        self.face_rec()
        # 提前加载识别器一次，避免每次预测重新加载（可根据需要调整）
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.recognizer.read("./data/Face_training/trainer.yml")
        except Exception as e:
            print("加载训练模型失败:", e)

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
        # 启动定时器采集图像
        self.timer_camera.start(10)

    def face_rec(self):
        # 已由 timer_camera 定时调用 show_camera
        pass

    def show_camera(self):
        try:
            frame = self.picam2.capture_array()
        except Exception as e:
            print("捕获图像失败:", e)
            return
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 加载级联文件（使用硬编码路径或封装函数）
        cascade = cv2.CascadeClassifier("./resources/haarcascades/haarcascade_frontalface_default.xml")
        faces = cascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            # 如果模型加载成功，则进行预测
            if hasattr(self, "recognizer"):
                id, confidence = self.recognizer.predict(gray[y:y+h, x:x+w])
                if confidence < 90:
                    label = NAMES[id]
                    conf_text = f"  {round(100 - confidence)}%"
                else:
                    label = "unknown"
                    conf_text = f"  {round(100 - confidence)}%"
                cv2.putText(frame, str(label), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                cv2.putText(frame, str(conf_text), (x+5, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 1)
        show = cv2.resize(frame, (960,720))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_face.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def slot_btn_back(self):
        from ui.menu_ui import Ui_Menu
        self.menu = Ui_Menu()
        self.menu.show()
        self.timer_camera.stop()
        self.picam2.stop()
        self.hide()
