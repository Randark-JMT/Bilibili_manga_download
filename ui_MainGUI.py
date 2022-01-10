# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainGUI.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(774, 625)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.formLayoutWidget = QWidget(self.centralwidget)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 431, 131))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.textEdit_2 = QTextEdit(self.formLayoutWidget)
        self.textEdit_2.setObjectName(u"textEdit_2")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.textEdit_2)

        self.textEdit = QTextEdit(self.formLayoutWidget)
        self.textEdit.setObjectName(u"textEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.textEdit)

        self.textEdit_3 = QTextEdit(self.formLayoutWidget)
        self.textEdit_3.setObjectName(u"textEdit_3")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.textEdit_3)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(620, 10, 121, 61))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(460, 10, 151, 61))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(460, 80, 281, 61))
        self.treeWidget = QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(10, 150, 751, 441))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bilibili\u6f2b\u753b\u4e0b\u8f7d\u5668  V1.4.0", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237Cookie\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6f2b\u753bID\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u8303\u56f4\uff1a", None))
#if QT_CONFIG(whatsthis)
        self.textEdit.setWhatsThis(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58Cookie", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2\u8d2d\u4e70\u60c5\u51b5", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u4e0b\u8f7d", None))
    # retranslateUi

