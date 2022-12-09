import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from resources.ui_MainGUI import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        version = "1.0.0"
        self.setWindowTitle("Bilibili漫画下载器  " + version)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
