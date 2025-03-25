# ui/manager_face_ui.py
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QProgressBar, QMessageBox
import cv2, threading, os, time
from utils.face_utils import detect_faces
from utils.constants import NAMES

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
        self.cap = cv2.VideoCapture(0)
        self.CAM_NUM = 0
        self.__flag_work = 0
        self.x = 0
        self.cap.set(4, 951)  # 设置宽度
        self.cap.set(3, 761)  # 设置高度
        self.timer_camera = QtCore.QTimer()
        self.timer_camera.timeout.connect(self.show_camera)

    def init_ui(self):
        self.resize(1280, 800)
        self.lab_face = QLabel(self)
        self.lab_face.setGeometry(15, 40, 960, 720)
        self.lab_face.setFrameShape(QtWidgets.QFrame.Box)
        self.lab_face.setText("")
        self.lab_ID = QLabel(self)
        self.lab_ID.setGeometry(10, 40, 31, 41)

        self.layoutWidget = QWidget(self)
        self.layoutWidget.setGeometry(1010, 350, 231, 251)
        self.gridLayout = QGridLayout(self.layoutWidget)
        for pos, text in zip([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,0)], 
                             ['1','2','3','4','5','6','7','8','9','0']):
            btn = QPushButton(text, self)
            btn.setFixedHeight(50)
            btn.setStyleSheet("QPushButton{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}")
            self.gridLayout.addWidget(btn, pos[0], pos[1])
            setattr(self, f"btn_{text}", btn)
        self.btn_del = QPushButton('del', self)
        self.btn_del.setFixedHeight(50)
        self.btn_del.setStyleSheet("QPushButton{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}")
        self.gridLayout.addWidget(self.btn_del, 3, 1, 1, 2)

        # GroupBox用于人脸录入
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setTitle("录入人脸")
        self.groupBox.setGeometry(990, 120, 281, 191)
        self.groupBox.setStyleSheet(
            "QGroupBox { border-width:2px; border-style:solid; border-color:lightGray; font: 75 20pt \"Aharoni\"; margin-top: 0.5ex; }"
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
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setGeometry(10, 150, 261, 31)
        self.btn_back = QPushButton("返回", self)
        self.btn_back.setGeometry(1090, 670, 81, 51)
        self.btn_back.setStyleSheet("font: 75 16pt;")

        # 绑定数字键按钮事件
        self.btn_0.clicked.connect(self.slot_btn_0)
        self.btn_1.clicked.connect(self.slot_btn_1)
        self.btn_2.clicked.connect(self.slot_btn_2)
        self.btn_3.clicked.connect(self.slot_btn_3)
        self.btn_4.clicked.connect(self.slot_btn_4)
        self.btn_5.clicked.connect(self.slot_btn_5)
        self.btn_6.clicked.connect(self.slot_btn_6)
        self.btn_7.clicked.connect(self.slot_btn_7)
        self.btn_8.clicked.connect(self.slot_btn_8)
        self.btn_9.clicked.connect(self.slot_btn_9)
        self.btn_del.clicked.connect(self.slot_btn_del)
        self.btn_back.clicked.connect(self.slot_btn_back)
        self.btn_enter.clicked.connect(self.slot_btn_enter)

    def slot_btn_back(self):
        from ui.login_ui import Ui_logon
        self.logon = Ui_logon()
        self.logon.show()
        self.timer_camera.stop()
        self.cap.release()
        self.hide()

    def face_rec(self):
        if not self.timer_camera.isActive():
            flag = self.cap.open(self.CAM_NUM)
            if not flag:
                QtWidgets.QMessageBox.warning(self, "Warning", "请检测相机与电脑是否连接正确", QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
        else:
            self.timer_camera.stop()
            self.cap.release()

    def show_camera(self):
        ret, image = self.cap.read()
        if ret:
            image = cv2.flip(image, -1)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (255,0,0), 2)
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
        print("线程出没！！！")
        print(self.Edit_ID.text())
        self.file = "./data/Face_data/"
        while True:
            ret, img = self.cap.read()
            img = cv2.flip(img, -1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray)
            if not os.path.exists(self.file):
                os.makedirs(self.file, exist_ok=True)
                os.chmod(self.file, 0o777)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)
                self.count += 1
                cv2.imwrite(f"{self.file}/User.{self.Edit_ID.text()}.{self.count}.png", gray[y:y+h, x:x+w])
            if self.count >= 60:
                print("OK!")
                break
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []
            self.progressBar.setProperty("value", 65)
            for imagePath in imagePaths:
                from PIL import Image
                PIL_img = Image.open(imagePath).convert('L')
                img_numpy = np.array(PIL_img, 'uint8')
                user_id = int(os.path.split(imagePath)[-1].split(".")[1])
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
