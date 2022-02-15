import os
import sys
import time
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, QThread, Signal, QObject, SignalInstance
from ui_MainGUI import Ui_MainWindow
from settings import cookie_file, download_path
import ctypes


class Thread_Login(QThread):  # 扫码登录线程
    signal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        from login import bzlogin
        bzlogin(self.signal.emit)


class Thread_Download(QThread):  # 下载线程
    signal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        from download import download_main
        from settings import comic_dic
        download_main(comic_dic["id"], comic_dic["range"], self.signal.emit)


class MainWindow(QMainWindow, Ui_MainWindow):
    @Slot()
    def check_purchase_staus(self):  # 检查购买情况
        from download import get_purchase_status
        manga_id = self.textEdit_2.toPlainText()
        if manga_id == "" or not manga_id.isnumeric():
            self.textBrowser.append("漫画ID输入错误，请核对后再次执行")
            return None
        data_re = get_purchase_status(manga_id, self.textBrowser)
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
        self.pushButton_3.setEnabled(False)
        if self.textEdit_2.toPlainText() == "" or not self.textEdit_2.toPlainText().isnumeric():
            self.textBrowser.append("漫画ID输入错误，请检查输入")
            return None
        if self.textEdit_3.toPlainText() == "":
            self.textBrowser.append("下载范围输入错误，请检查输入")
            return None
        from settings import comic_dic
        comic_dic["id"] = self.textEdit_2.toPlainText()
        comic_dic["range"] = self.textEdit_3.toPlainText()
        self.thread_download.start()
        # 这里传递了self对象，来达到了跨函数控制窗体的可能

    @Slot()
    def login_qrcode(self):  # 登录模块
        self.pushButton.setEnabled(False)
        self.thread_login.start()

    @Slot()
    def download_manga_stop(self):
        self.thread_download.terminate()
        self.textBrowser.append("下载任务已被中断")
        self.pushButton_3.setEnabled(True)

    @Slot(str)
    def log_append(self, words):  # 日志输出，用槽函数接受信号
        if words == "0xe1":
            self.pushButton.setEnabled(True)
        elif words == "0xe2":
            self.pushButton_2.setEnabled(True)
        elif words == "0xe3":
            self.pushButton_3.setEnabled(True)
        else:
            self.textBrowser.append(words)

    @Slot()
    def log_scroll_down(self):
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    @Slot()
    def log_scroll_clear(self):
        self.textBrowser.setText("")

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.check_datafile()
        self.setAcceptDrops(True)
        # 漫画信息窗口-初始化

        self.thread_login = Thread_Login()
        self.thread_login.signal.connect(self.log_append)
        self.thread_download = Thread_Download()
        self.thread_download.signal.connect(self.log_append)
        # 日志输出与信号系统相连接

        self.pushButton_2.clicked.connect(self.check_purchase_staus)  # 检查购买按钮
        self.pushButton.clicked.connect(self.login_qrcode)  # 扫码登录按钮
        self.pushButton_3.clicked.connect(self.download_manga)  # 开始下载按钮
        self.pushButton_6.clicked.connect(self.download_manga_stop)  # 下载终止按钮
        self.pushButton_5.clicked.connect(self.log_scroll_down)
        self.pushButton_4.clicked.connect(self.log_scroll_clear)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
