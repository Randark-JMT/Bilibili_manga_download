import os
import sys
import threading
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot
from ui_MainGUI_Pyside6 import Ui_MainWindow
from settings import cookie_file, download_path


def check_datafile():
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(cookie_file):
        file = open(cookie_file, 'w')
        file.close()


class MainWindow(QMainWindow, Ui_MainWindow):
    @Slot()
    def check_purchase_staus(self):
        from downloader import download_purchase_status
        download_purchase_status(self.textEdit_3.toPlainText(), self.textEdit.toPlainText(), self.treeWidget)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 漫画信息窗口-初始化
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['Key', 'Value'])
        self.pushButton_2.clicked.connect(self.check_purchase_staus)


if __name__ == "__main__":
    check_datafile()
    app = QApplication()
    app.setWindowIcon(QIcon("main.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
