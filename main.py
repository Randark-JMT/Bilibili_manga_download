import os
import sys
import time
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, QThread, Signal
from ui_MainGUI import Ui_MainWindow
import Bilibili.settings
import logging
import json


class Log_Recoreer:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


class Thread_Login(QThread):
    """
    扫码登录线程
    """
    signal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        from Bilibili.login import bzlogin
        bzlogin(self.signal.emit)


class Thread_Download(QThread):
    """
    下载线程，传入漫画ID和下载范围
    """
    signal = Signal(str)

    def __init__(self, comic_id, comic_range):
        super().__init__()
        self.comic_id = comic_id
        self.comic_range = comic_range

    def run(self):
        from Bilibili.download import download_main
        download_main(self.comic_id, self.comic_range, self.signal.emit)


class MainWindow(QMainWindow, Ui_MainWindow):

    @Slot()
    def check_datafile(self):  # 启动时检查数据文件
        if not os.path.exists(Bilibili.settings.download_path):
            os.makedirs(Bilibili.settings.download_path)
        if not os.path.exists(Bilibili.settings.setting_file):
            f = open(Bilibili.settings.setting_file, 'a+')
            f.close()
        text = Bilibili.settings.settintfile_read()
        if len(text) > 0:
            properties = json.loads(text)

    @Slot()
    def get_manga_id(self) -> int:
        """
        链接解析
        """
        from urllib.parse import urlparse
        url = str(self.textEdit_2.toPlainText())
        url = urlparse(url)
        if url.netloc == 'manga.bilibili.com':
            if str(url.path).find('mc') == -1:
                self.textBrowser.append("未检测到漫画信息")
                return -1
        else:
            self.textBrowser.append("链接输入错误，非B漫链接")
            return -1
        return int(str(url.path).split("/")[2][2:])

    @Slot()
    def check_purchase_staus(self):  # 检查购买情况
        from Bilibili.download import get_purchase_status
        manga_id = self.get_manga_id()
        if manga_id == -1:
            self.textBrowser.append("漫画ID输入错误，请核对后再次执行")
            return None
        data_re = get_purchase_status(manga_id, self.textBrowser.append)
        if data_re is None:
            return None
        # TODO 做个防呆，避免用户非法输入
        self.textBrowser.append("查询  " + str(data_re[0][0]) + "-" + data_re[0][1])
        self.textBrowser.append("查询时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for data in data_re[1:]:
            self.textBrowser.append(data[0] + data[1])

    @Slot()
    def download_manga(self):  # 下载
        self.pushButton_3.setEnabled(False)
        if self.textEdit_2.toPlainText() == "" or not self.textEdit_2.toPlainText().isnumeric():
            self.textBrowser.append("漫画ID输入错误，请检查输入")
            self.pushButton_3.setEnabled(True)
            return None
        if self.textEdit_3.toPlainText() == "":
            self.textBrowser.append("下载范围输入错误，请检查输入")
            self.pushButton_3.setEnabled(True)
            return None
        self.thread_download = Thread_Download(self.textEdit_2.toPlainText(), self.textEdit_3.toPlainText())
        self.thread_download.signal.connect(self.log_append)
        self.thread_download.start()

    @Slot()
    def login_qrcode(self):  # 登录
        self.thread_login = Thread_Login()
        self.thread_login.signal.connect(self.log_append)
        self.pushButton.setEnabled(False)
        self.thread_login.start()

    @Slot()
    def download_manga_stop(self):  # 下载中断
        self.thread_download.terminate()
        self.textBrowser.append("下载任务已被中断")
        self.pushButton_3.setEnabled(True)

    @Slot(str)
    def log_append(self, status, message):  # 日志输出，用槽函数接受信号
        if status == "0xe1":
            self.pushButton.setEnabled(True)
        if status == "0xe2":
            self.pushButton_2.setEnabled(True)
        if status == "0xe3":
            self.pushButton_3.setEnabled(True)
        self.textBrowser.append(message)

    @Slot()
    def log_scroll_down(self):  # 日志下滑
        self.textBrowser.moveCursor(self.textBrowser.textCursor().End)

    @Slot()
    def log_clear(self):  # 日志清空
        self.textBrowser.setText("")

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.thread_login = None
        self.thread_download = None
        self.setupUi(self)
        from Bilibili.settings import version
        self.setWindowTitle("Bilibili漫画下载器  " + version)
        self.check_datafile()
        # 漫画信息窗口-初始化

        self.pushButton_2.clicked.connect(self.check_purchase_staus)  # 检查购买按钮
        self.pushButton.clicked.connect(self.login_qrcode)  # 扫码登录按钮
        self.pushButton_3.clicked.connect(self.download_manga)  # 开始下载按钮
        self.pushButton_6.clicked.connect(self.download_manga_stop)  # 下载终止按钮
        self.pushButton_5.clicked.connect(self.log_scroll_down)  # 日志框下滑按钮
        self.pushButton_4.clicked.connect(self.log_clear)  # 日志清零


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
