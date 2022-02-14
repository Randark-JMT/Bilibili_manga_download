import os
import sys
import time
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, QThread, Signal, QObject,SignalInstance
from ui_MainGUI import Ui_MainWindow
from settings import cookie_file, download_path


class Thread_Login(QThread):  # 扫码登录线程
    signal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        from Bili_login import bzlogin
        bzlogin(self.signal.emit)


class MainWindow(QMainWindow, Ui_MainWindow):
    @Slot()
    def check_purchase_staus(self):  # 检查购买情况
        from download import get_purchase_status
        data_re = get_purchase_status(self.textEdit_3.toPlainText(), self.textBrowser)
        if data_re is None:
            return None
        # TODO 做个防呆，避免用户非法输入
        self.textBrowser.append("查询  " + str(data_re[0][0]) + "-" + data_re[0][1])
        self.textBrowser.append("查询时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for data in data_re[1:]:
            self.textBrowser.append(data[0] + data[1])

    @Slot()
    def check_datafile(self):  # 检查数据文件
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        if not os.path.exists(cookie_file):
            file = open(cookie_file, 'w')
            file.close()

    @Slot()
    def download_manga(self):  # 下载
        from download import download_main
        download_main(self, self.textEdit_2.toPlainText(), self.textEdit_3.toPlainText(), self.textBrowser)
        # 这里传递了self对象，来达到了跨函数控制窗体的可能

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.check_datafile()
        self.setAcceptDrops(True)
        # 漫画信息窗口-初始化

        self.thread_login = Thread_Login()
        self.thread_login.signal.connect(self.log_append)
        self.pushButton_2.clicked.connect(self.check_purchase_staus)  # 检查购买按钮
        self.pushButton.clicked.connect(self.login_qrcode)  # 扫码登录按钮
        self.pushButton_3.clicked.connect(self.download_manga)  # 开始下载按钮

    @Slot(str)
    def log_append(self, words):
        self.textBrowser.append(words)
        print(words)

    def login_qrcode(self):
        self.thread_login.start()


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QIcon("main.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
