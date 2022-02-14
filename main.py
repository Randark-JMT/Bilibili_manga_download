import os
import sys
import time
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot
from ui_MainGUI import Ui_MainWindow
from settings import cookie_file, download_path


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
    def cookie_renovate(self):  # 保存用户Cookie
        with open(cookie_file, 'w') as file:
            sessdata = self.textEdit.toPlainText()
            file.write(sessdata)
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, "储存Cookie 成功")
        root.setText(1, "执行时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    @Slot()
    def check_datafile(self):  # 检查数据文件
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        if not os.path.exists(cookie_file):
            file = open(cookie_file, 'w')
            file.close()

    @Slot()
    def download_manga(self):
        from download import download_main
        download_main(self, self.textEdit_3.toPlainText(), self.textEdit_2.toPlainText(), self.treeWidget)
        # 这里传递了self对象，来达到了跨函数控制窗体的可能

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.check_datafile()
        print(type(self))
        # 漫画信息窗口-初始化
        self.setAcceptDrops(True)
        self.pushButton_2.clicked.connect(self.check_purchase_staus)
        self.pushButton.clicked.connect(self.cookie_renovate)
        self.pushButton_3.clicked.connect(self.download_manga)


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QIcon("main.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
