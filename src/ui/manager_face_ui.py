# ui/manager_face_ui.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QProgressBar, QMessageBox
import cv2, threading, os, time
import numpy as np
from PIL import Image
from picamera2 import Picamera2
from utils.face_utils import detect_faces
from utils.constants import NAMES

class Ui_manager_face(QWidget):
    def __init__(self):
        super(Ui_manager_face, self).__init__()
        self.ID_num = ""
        self.count = 0
        self.step = 0
        self.training_in_progress = False  # 训练期间标志
        self.init_ui()
        self.camera_init()
        self.face_rec()

    def camera_init(self):
        # 使用 picamera2 替代 cv2.VideoCapture
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(main={"size": (640, 480)})
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
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        positions = [(i, j) for i in range(4) for j in range(3)]
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
        # 停止定时器与摄像头采集
        self.timer_camera.stop()
        self.picam2.stop()
        self.hide()

    def face_rec(self):
        # 启动定时器采集预览图像
        self.timer_camera.start(30)

    def show_camera(self):
        # 训练期间不调用预览检测
        if self.training_in_progress:
            return
        try:
            frame = self.picam2.capture_array()
        except Exception as e:
            print("捕获图像失败:", e)
            return
        if frame is None or frame.size == 0:
            print("捕获到空图像")
            return
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray)
        if faces is not None:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        show = cv2.resize(frame, (960, 720))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.lab_face.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def slot_btn_enter(self):
        self.count = 0
        self.step = 0
        self.training_in_progress = False  # 初始时不是训练状态
        self.frame_counter = 0  # 初始化帧计数器
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
        desired_samples = 60
        if not os.path.exists(self.file):
            os.makedirs(self.file, exist_ok=True)
            os.chmod(self.file, 0o777)
        # 采集样本，每10帧处理一次
        while self.count < desired_samples:
            try:
                img = self.picam2.capture_array()
            except Exception as e:
                print("线程采集图像失败:", e)
                continue
            if img is None or img.size == 0:
                print("采集到空图像")
                continue
            self.frame_counter += 1
            if self.frame_counter % 10 != 0:
                continue
            img = cv2.flip(img, -1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray)
            if faces is None or len(faces) == 0:
                print("未检测到人脸")
                continue
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                self.count += 1
                sample_filename = f"{self.file}/User.{self.Edit_ID.text()}.{self.count}.png"
                cv2.imwrite(sample_filename, gray[y:y+h, x:x+w])
                print(f"保存样本: {sample_filename}, 当前样本数: {self.count}")
                if self.count >= desired_samples:
                    break
        print("样本采集完成!")
        
        # 停止预览定时器，避免在训练期间调用 detect_faces
        QtCore.QMetaObject.invokeMethod(self.timer_camera, "stop", QtCore.Qt.QueuedConnection)
        self.training_in_progress = True

        # 训练模型
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.startswith("User.")]
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
                detected_faces = detect_faces(img_numpy)
                if detected_faces is None or len(detected_faces) == 0:
                    print("图片中未检测到人脸:", imagePath)
                    continue
                for (x, y, w, h) in detected_faces:
                    faceSamples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(user_id)
            return faceSamples, ids

        self.progressBar.setProperty("value", 75)
        print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces, ids = getImagesAndLabels(self.file)
        if len(faces) == 0:
            print("未采集到有效人脸样本，无法训练模型")
            self.training_in_progress = False
            return
        recognizer.train(faces, np.array(ids))
        self.progressBar.setProperty("value", 85)
        training_dir = "./data/Face_training/"
        if not os.path.exists(training_dir):
            os.makedirs(training_dir, exist_ok=True)
            os.chmod(training_dir, 0o777)
        trainer_path = f"{training_dir}/trainer.yml"
        recognizer.write(trainer_path)
        print("\n [INFO] {0} faces trained. 模型保存在 {1}".format(len(set(ids)), trainer_path))
        self.progressBar.setProperty("value", 100)
        
        self.training_in_progress = False
