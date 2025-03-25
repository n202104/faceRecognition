# ui/login_ui.py
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt

# 自定义 QLineEdit，当鼠标释放时发出 clicked 信号
class mylineedit(QLineEdit):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super(mylineedit, self).mouseReleaseEvent(event)

class Ui_logon(QWidget):
    clicked = pyqtSignal()
    def __init__(self):
        super(Ui_logon, self).__init__()
        self.ID_num = ""
        self.key_num = ""
        self.selected = None
        self.init_ui()

    def init_ui(self):
        self.resize(1280, 800)
        self.lab_ID = QLabel('账号', self)
        self.lab_ID.setGeometry(380, 130, 71, 41)
        self.lab_key = QLabel('密码', self)
        self.lab_key.setGeometry(380, 200, 71, 41)
        self.Edit_ID = mylineedit(self)
        self.Edit_ID.setGeometry(470, 130, 411, 41)
        self.Edit_key = mylineedit(self)
        self.Edit_key.setGeometry(470, 200, 411, 41)
        self.Edit_key.setEchoMode(QLineEdit.Password)
        self.selected = self.Edit_ID

        self.btn_logon = QPushButton('登录', self)
        self.btn_logon.setGeometry(490, 270, 91, 51)
        self.btn_back = QPushButton('返回', self)
        self.btn_back.setGeometry(690, 270, 91, 51)

        # 数字键盘（虽然原代码定义了，但在本示例中我们不在此处实现完整键盘，而是在其它模块中使用）
        # 如果需要，可按需要补充数字键盘部件

        style_lbl = "QLabel{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}"
        style_edit = "QLineEdit{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}"
        style_btn = "QPushButton{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}"
        self.lab_ID.setStyleSheet(style_lbl)
        self.lab_key.setStyleSheet(style_lbl)
        self.Edit_ID.setStyleSheet(style_edit)
        self.Edit_key.setStyleSheet(style_edit)
        self.btn_logon.setStyleSheet(style_btn)
        self.btn_back.setStyleSheet(style_btn)
        self.btn_logon.setFixedHeight(50)
        self.btn_back.setFixedHeight(50)

        self.Edit_ID.clicked.connect(self.changeEdit_ID)
        self.Edit_key.clicked.connect(self.changeEdit_key)
        self.btn_back.clicked.connect(self.slot_btn_back)
        self.btn_logon.clicked.connect(self.slot_btn_logon)

    def changeEdit_ID(self):
        self.selected = self.Edit_ID

    def changeEdit_key(self):
        self.selected = self.Edit_key

    def slot_btn_back(self):
        from ui.menu_ui import Ui_Menu
        self.menu = Ui_Menu()
        self.menu.show()
        self.hide()

    def slot_btn_logon(self):
        # 管理员账号密码均为 "1"
        if self.Edit_ID.text() == "1" and self.Edit_key.text() == "1":
            from ui.manager_face_ui import Ui_manager_face
            self.manager_face = Ui_manager_face()
            self.manager_face.show()
            self.hide()
        else:
            QMessageBox.warning(self, "提示", "账号或密码错误！", QMessageBox.Close)
