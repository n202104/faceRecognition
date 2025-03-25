# ui/manager_face_ui.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QProgressBar, QMessageBox
import threading, os, time
import cv2, numpy as np
from PIL import Image
from picamera2 import Picamera2
from utils.face_utils import detect_faces
from utils.constants import NAMES
# 注意：在实际项目中，可以将 picamera2 配置参数及分辨率统一放在常量中

class Ui_manager_face(QWidget):
    def __init__(self):
        super(Ui_manager_face, self).__init__()
        self.ID_num = ""
        self.count = 0
        self.step = 0
        self.init_ui()
        self.camera_init()
        self.face_rec()

    def camera_init(self):
        # 创建并配置 picamera2
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": (640,480)})
        self.picam2.configure(config)
        self.picam2.start()
        time.sleep(1)  # 摄像头预热
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)

    def init_ui(self):
        self.resize(1280, 800)
        # 视频显示区域
        self.lab_face = QLabel(self)
        self.lab_face.setGeometry(15, 40, 960, 720)
        self.lab_face.setFrameShape(QtWidgets.QFrame.Box)
        self.lab_face.setText("")
        
        # 数字键盘区域（使用栅格布局）
        self.layoutWidget = QWidget(self)
        self.layoutWidget.setGeometry(1010, 350, 231, 251)
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.buttons = {}
        numbers = ['1','2','3','4','5','6','7','8','9','0']
        positions = [(i,j) for i in range(4) for j in range(3)]
        for idx, num in enumerate(numbers):
            btn = QPushButton(num, self)
            btn.setFixedHeight(50)
            btn.setStyleSheet("QPushButton { color: rgb(0,0,0); font-size: 30px; font-family: Roman times; }")
            pos = positions[idx]
            self.gridLayout.addWidget(btn, pos[0], pos[1])
            self.buttons[num] = btn
        self.btn_del = QPushButton('del', self)
        self.btn_del.setFixedHeight(50)
        self.btn_del.setStyleSheet("QPushButton { color: rgb(0,0,0); font-size: 30px; font-family: Roman times; }")
        self.gridLayout.addWidget(self.btn_del, 3, 1, 1, 2)

        # GroupBox 用于人脸录入
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setTitle("录入人脸")
        self.groupBox.setGeometry(990, 120, 281, 191)
        self.groupBox.setStyleSheet(
            "QGroupBox { border-width:2px; border-style:solid; border-color:lightGray; font: 75 20pt 'Aharoni'; margin-top: 0.5ex; }"
            "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; left:10px; margin-left: 0px; padding:0px; }"
        )
        self.lab_ID_in_group = QLabel(self.groupBox)
        self.lab_ID_in_group.setText("ID")
        self.lab_ID_in_group.setGeometry(10, 40, 31, 41)
        self.lab_ID_in_group.setStyleSheet("font: 18pt;")
        self.Edit_ID = QLineEdit(self.groupBox)
        self.Edit_ID.setGeometry(50, 40, 221, 41)
        self.Edit_ID.setStyleSheet("font: 18pt;")
        self.btn_enter = QPushButton("开始录入", self.groupBox)
        self.btn_enter.setGeometry(80, 90, 121, 51)
        self.btn_enter.setStyleSheet("font: 75 16pt;")
        self.progressBar = QProgressBar(self.groupBox)
        self.progressBar.setGeometry(10, 150, 261, 31)
        
        self.btn_back = QPushButton("返回", self)
        self.btn_back.setGeometry(1090, 670, 81, 51)
        self.btn_back.setStyleSheet("font: 75 16pt;")

        # 数字键盘事件绑定
        for num in numbers:
            self.buttons[num].clicked.connect(lambda checked, n=num: self.append_digit(n))
        self.btn_del.clicked.connect(self.delete_digit)
        self.btn_back.clicked.connect(self.slot_btn_back)
        self.btn_enter.clicked.connect(self.slot_btn_enter)

    def append_digit(self, digit):
        self.ID_num += digit
        self.Edit_ID.setText(self.ID_num)

    def delete_digit(self):
        self.ID_num = self.ID_num[:-1]
        self.Edit_ID.setText(self.ID_num)

    def slot_btn_back(self):
        from ui.login_ui import Ui_logon
        self.logon = Ui_logon()
        self.logon.show()
        self.timer_camera.stop()
        self.picam2.stop()
        self.hide()

    def face_rec(self):
        # 启动定时器采集预览图像
        self.timer_camera.start(30)

    def show_camera(self):
        try:
            image = self.picam2.capture_array()
        except Exception as e:
            print("捕获图像失败:", e)
            return
        # 翻转图像（根据需要）
        image = cv2.flip(image, -1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        show = cv2.resize(image, (960,720))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_face.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def slot_btn_enter(self):
        self.count = 0
        self.step = 0
        self.thread = threading.Thread(target=self.thread_pic)
        self.thread.start()
        self.timer = QtCore.QBasicTimer()
        self.timer.start(100, self)

    def timerEvent(self, event):
        if self.step > 58:
            self.timer.stop()
            return
        self.step = self.count + 1
        self.progressBar.setValue(self.count)

    def thread_pic(self):
        print("线程开始采集样本...")
        print("用户 ID:", self.Edit_ID.text())
        self.file = "./data/Face_data/"
        while True:
            try:
                img = self.picam2.capture_array()
            except Exception as e:
                print("线程采集图像失败:", e)
                continue
            img = cv2.flip(img, -1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray)
            if not os.path.exists(self.file):
                os.makedirs(self.file, exist_ok=True)
                os.chmod(self.file, 0o777)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                self.count += 1
                cv2.imwrite(f"{self.file}/User.{self.Edit_ID.text()}.{self.count}.png", gray[y:y+h, x:x+w])
            if self.count >= 10:         #拍照次数
                print("样本采集完成!")
                break
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []
            self.progressBar.setProperty("value", 65)
            for imagePath in imagePaths:
                try:
                    PIL_img = Image.open(imagePath).convert('L')
                except Exception as e:
                    print("读取图片失败:", e)
                    continue
                img_numpy = np.array(PIL_img, 'uint8')
                try:
                    user_id = int(os.path.split(imagePath)[-1].split(".")[1])
                except Exception as e:
                    print("解析文件名失败:", e)
                    continue
                faces = detect_faces(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(user_id)
            return faceSamples, ids
        self.progressBar.setProperty("value", 75)
        print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(self.file)
        recognizer.train(faces, np.array(ids))
        self.progressBar.setProperty("value", 85)
        training_dir = "./data/Face_training/"
        if not os.path.exists(training_dir):
            os.makedirs(training_dir, exist_ok=True)
            os.chmod(training_dir, 0o777)
        recognizer.write(f"{training_dir}/trainer.yml")
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(set(ids))))
        self.progressBar.setProperty("value", 100)
