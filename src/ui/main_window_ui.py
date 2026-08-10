# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QSizePolicy, QToolBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(507, 420)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.game_cards_list_widget = QListWidget(self.centralwidget)
        self.game_cards_list_widget.setObjectName(u"game_cards_list_widget")
        self.game_cards_list_widget.setIconSize(QSize(150, 150))
        self.game_cards_list_widget.setMovement(QListView.Movement.Static)
        self.game_cards_list_widget.setResizeMode(QListView.ResizeMode.Adjust)
        self.game_cards_list_widget.setLayoutMode(QListView.LayoutMode.SinglePass)
        self.game_cards_list_widget.setSpacing(12)
        self.game_cards_list_widget.setGridSize(QSize(180, 200))
        self.game_cards_list_widget.setViewMode(QListView.ViewMode.IconMode)
        self.game_cards_list_widget.setUniformItemSizes(False)

        self.gridLayout_2.addWidget(self.game_cards_list_widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

