# main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.menu_ui import Ui_Menu

def main():
    app = QApplication(sys.argv)
    main_window = Ui_Menu()  # 打开主菜单界面
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
