import sys
from PySide6.QtWidgets import QMainWindow, QApplication
from ui_MainGUI import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    pass


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
