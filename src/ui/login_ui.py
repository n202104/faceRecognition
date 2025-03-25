# ui/login_ui.py
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt

# 自定义 QLineEdit，用于点击时发出信号
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

        # 数字按键
        self.btn_1 = QPushButton('1', self)
        self.btn_2 = QPushButton('2', self)
        self.btn_3 = QPushButton('3', self)
        self.btn_4 = QPushButton('4', self)
        self.btn_5 = QPushButton('5', self)
        self.btn_6 = QPushButton('6', self)
        self.btn_7 = QPushButton('7', self)
        self.btn_8 = QPushButton('8', self)
        self.btn_9 = QPushButton('9', self)
        self.btn_0 = QPushButton('0', self)
        self.btn_del = QPushButton('del', self)

        # 数字键盘容器，使用栅格布局
        self.layoutWidget = QWidget(self)
        self.layoutWidget.setGeometry(491, 404, 291, 251)
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.addWidget(self.btn_1, 0, 0)
        self.gridLayout.addWidget(self.btn_2, 0, 1)
        self.gridLayout.addWidget(self.btn_3, 0, 2)
        self.gridLayout.addWidget(self.btn_4, 1, 0)
        self.gridLayout.addWidget(self.btn_5, 1, 1)
        self.gridLayout.addWidget(self.btn_6, 1, 2)
        self.gridLayout.addWidget(self.btn_7, 2, 0)
        self.gridLayout.addWidget(self.btn_8, 2, 1)
        self.gridLayout.addWidget(self.btn_9, 2, 2)
        self.gridLayout.addWidget(self.btn_0, 3, 0)
        self.gridLayout.addWidget(self.btn_del, 3, 1, 1, 2)

        # 设置控件样式
        style_lbl = "QLabel{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}"
        style_edit = "QLineEdit{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}"
        style_btn = "QPushButton{color:rgb(0,0,0,255); font-size:30px; font-family:Roman times;}"
        self.lab_ID.setStyleSheet(style_lbl)
        self.lab_key.setStyleSheet(style_lbl)
        self.Edit_ID.setStyleSheet(style_edit)
        self.Edit_key.setStyleSheet(style_edit)
        for btn in [self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5,
                    self.btn_6, self.btn_7, self.btn_8, self.btn_9, self.btn_0,
                    self.btn_del, self.btn_logon, self.btn_back]:
            btn.setStyleSheet(style_btn)
            btn.setFixedHeight(50)

        # 绑定 mylineedit 点击事件
        self.Edit_ID.clicked.connect(self.changeEdit_ID)
        self.Edit_key.clicked.connect(self.changeEdit_key)
        # 按钮事件绑定
        self.btn_back.clicked.connect(self.slot_btn_back)
        self.btn_logon.clicked.connect(self.slot_btn_logon)
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

    def changeEdit_ID(self):
        self.selected = self.Edit_ID

    def changeEdit_key(self):
        self.selected = self.Edit_key

    def slot_btn_back(self):
        # 延迟导入避免循环引用
        from ui.menu_ui import Ui_Menu
        self.menu = Ui_Menu()
        self.menu.show()
        self.hide()

    def slot_btn_logon(self):
        if self.Edit_ID.text() == "1" and self.Edit_key.text() == "1":
            from ui.manager_face_ui import Ui_manager_face
            self.manager_face = Ui_manager_face()
            self.manager_face.show()
            self.hide()
        else:
            QMessageBox.warning(self, "提示", "账号或密码错误！", QMessageBox.Close)

    def slot_btn_0(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_0.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_0.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_1(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_1.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_1.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_2(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_2.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_2.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_3(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_3.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_3.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_4(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_4.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_4.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_5(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_5.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_5.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_6(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_6.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_6.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_7(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_7.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_7.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_8(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_8.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_8.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_9(self):
        if self.selected == self.Edit_ID:
            self.ID_num += self.btn_9.text()
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num += self.btn_9.text()
            self.Edit_key.setText(self.key_num)

    def slot_btn_del(self):
        if self.selected == self.Edit_ID:
            self.ID_num = self.ID_num[:-1]
            self.Edit_ID.setText(self.ID_num)
        elif self.selected == self.Edit_key:
            self.key_num = self.key_num[:-1]
            self.Edit_key.setText(self.key_num)
