# ui/menu_ui.py
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt

def open_login_ui():
    from ui.login_ui import Ui_logon
    return Ui_logon()

def open_user_face_ui():
    from ui.user_face_ui import Ui_face_reco
    return Ui_face_reco()

class Ui_Menu(QWidget):
    def __init__(self):
        super(Ui_Menu, self).__init__()
        self.label = QLabel('欢迎使用人脸识别门禁系统', self)
        self.btn_ordinary = QPushButton('普通用户', self)
        self.btn_admin = QPushButton('管理员', self)
        self.init_ui()

    def init_ui(self):
        self.resize(1280, 800)
        self.label.move(140, 200)
        self.label.setStyleSheet("QLabel{color:rgb(0,0,0,255); font-size:82px;font-weight:bold; font-family:Roman times;}")
        self.btn_ordinary.setGeometry(550, 420, 181, 61)
        self.btn_admin.setGeometry(550, 510, 181, 61)
        self.btn_ordinary.setStyleSheet("QPushButton{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}")
        self.btn_admin.setStyleSheet("QPushButton{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}")
        self.btn_admin.clicked.connect(self.slot_btn_admin)
        self.btn_ordinary.clicked.connect(self.slot_btn_ordinary)

    def slot_btn_admin(self):
        self.logon = open_login_ui()
        self.logon.show()
        self.hide()

    def slot_btn_ordinary(self):
        self.face_reco = open_user_face_ui()
        self.face_reco.show()
        self.hide()
