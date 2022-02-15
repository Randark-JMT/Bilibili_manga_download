# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainGUI.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTextBrowser,
    QTextEdit, QWidget)
import main_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(815, 652)
        MainWindow.setMinimumSize(QSize(770, 610))
        font = QFont()
        font.setPointSize(5)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/main.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QSize(25, 25))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_3.setFont(font1)

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        font2 = QFont()
        font2.setPointSize(10)
        self.textBrowser.setFont(font2)

        self.gridLayout.addWidget(self.textBrowser, 3, 0, 1, 7)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 70))
        self.pushButton_3.setMaximumSize(QSize(16777215, 70))
        self.pushButton_3.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_3, 1, 3, 1, 4)

        self.textEdit_3 = QTextEdit(self.centralwidget)
        self.textEdit_3.setObjectName(u"textEdit_3")
        self.textEdit_3.setMinimumSize(QSize(0, 60))
        self.textEdit_3.setMaximumSize(QSize(16777215, 70))
        self.textEdit_3.setFont(font2)

        self.gridLayout.addWidget(self.textEdit_3, 1, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 0))
        self.label_2.setFont(font1)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 70))
        self.pushButton.setMaximumSize(QSize(16777215, 70))
        self.pushButton.setFont(font2)

        self.gridLayout.addWidget(self.pushButton, 0, 6, 1, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(144, 70))
        self.pushButton_2.setMaximumSize(QSize(16777215, 70))
        self.pushButton_2.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_2, 0, 3, 1, 3)

        self.textEdit_2 = QTextEdit(self.centralwidget)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setMaximumSize(QSize(16777215, 70))
        self.textEdit_2.setFont(font2)

        self.gridLayout.addWidget(self.textEdit_2, 0, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(70, 70))
        self.pushButton_4.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_4, 4, 0, 1, 1)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(0, 70))
        self.pushButton_5.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_5, 4, 1, 1, 1)

        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(0, 70))
        self.pushButton_6.setFont(font2)

        self.gridLayout.addWidget(self.pushButton_6, 4, 3, 1, 4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bilibili\u6f2b\u753b\u4e0b\u8f7d\u5668  V1.4.0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u8303\u56f4\uff1a", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u4e0b\u8f7d", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6f2b\u753bID\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u626b\u7801\u767b\u5f55", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2\u8d2d\u4e70\u60c5\u51b5", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a\u65e5\u5fd7", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"\u6ed1\u81f3\u65e5\u5fd7\u5e95\u90e8", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u4e0b\u8f7d", None))
    # retranslateUi

