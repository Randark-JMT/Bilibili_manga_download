import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, Slot
from ui_MainGUI_Pyside6 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def hello(self):
        self.label_3.setText("test")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
