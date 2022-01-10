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
        # QMessageBox.warning(self, "提示", "注意，此操作需要一定耗时，请耐心等待，不要随便关闭窗口\n开发者正在尝试解决此问题，请谅解。")
        from downloader import get_purchase_status
        data_rt = get_purchase_status(self.textEdit_3.toPlainText(), self.textEdit.toPlainText(), self.treeWidget)
        if data_rt == None:
            return None
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, "查询  " + str(data_rt[0][0]) + "-" + data_rt[0][1])
        root.setText(1, "查询时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for data in data_rt[1:]:
            msg = QTreeWidgetItem(root)
            msg.setText(0, data[0])
            msg.setText(1, data[1])
        self.treeWidget.expandItem(root)
        self.treeWidget.scrollToBottom()

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
        with open(cookie_file, 'r') as file:
            sessdata = file.read()
            self.textEdit.setText(sessdata)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.check_datafile()
        # 漫画信息窗口-初始化
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['字段', '数据'])
        self.treeWidget.setColumnWidth(0, 300)
        self.pushButton_2.clicked.connect(self.check_purchase_staus)
        self.pushButton.clicked.connect(self.cookie_renovate)


if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QIcon("main.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
