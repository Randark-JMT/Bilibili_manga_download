from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from PySide6.QtCore import Slot, QThread, Signal, QObject, SignalInstance
import sys
import time


# 继承QThread


class Thread_2(QThread):  # 线程2
    _signal = Signal()

    def __init__(self):
        super().__init__()

    def run(self):
        values = ["a", "b", "c", "d", "e"]
        for i in values:
            print(i)
            time.sleep(0.5)
        self._signal.emit()


class MyWin(QWidget):
    def __init__(self):
        super().__init__()
        # 按钮初始化

        self.btn_2 = QPushButton('按钮2', self)
        self.btn_2.move(120, 120)
        self.btn_2.clicked.connect(self.click_2)  # 绑定槽函数

    def click_2(self):
        self.btn_2.setEnabled(False)
        self.thread_2 = Thread_2()
        self.thread_2._signal.connect(self.set_btn)
        self.thread_2.start()

    def set_btn(self):
        self.btn_2.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = MyWin()
    myshow.show()
    sys.exit(app.exec_())
