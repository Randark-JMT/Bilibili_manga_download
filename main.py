import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from resources.ui_MainGUI import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.thread_login = None
        self.thread_download = None
        self.setupUi(self)
        version = "1.0.0"
        self.setWindowTitle("Bilibili漫画下载器  " + version)
        # 漫画信息窗口-初始化


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
