# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(719, 518)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.side_bar = QFrame(self.centralwidget)
        self.side_bar.setObjectName(u"side_bar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.side_bar.sizePolicy().hasHeightForWidth())
        self.side_bar.setSizePolicy(sizePolicy)
        self.side_bar.setMinimumSize(QSize(60, 0))
        self.side_bar.setMaximumSize(QSize(200, 16777215))
        self.side_bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.side_bar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_toggle = QPushButton(self.side_bar)
        self.btn_toggle.setObjectName(u"btn_toggle")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        self.btn_toggle.setIcon(icon)

        self.verticalLayout_2.addWidget(self.btn_toggle)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_search = QToolButton(self.side_bar)
        self.btn_search.setObjectName(u"btn_search")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_search.sizePolicy().hasHeightForWidth())
        self.btn_search.setSizePolicy(sizePolicy1)
        self.btn_search.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind))
        self.btn_search.setIcon(icon1)
        self.btn_search.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.btn_search.setAutoRaise(False)

        self.verticalLayout.addWidget(self.btn_search)

        self.btn_home = QToolButton(self.side_bar)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy1.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy1)
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))
        self.btn_home.setIcon(icon2)
        self.btn_home.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout.addWidget(self.btn_home)

        self.btn_library = QToolButton(self.side_bar)
        self.btn_library.setObjectName(u"btn_library")
        sizePolicy1.setHeightForWidth(self.btn_library.sizePolicy().hasHeightForWidth())
        self.btn_library.setSizePolicy(sizePolicy1)
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.InputGaming))
        self.btn_library.setIcon(icon3)
        self.btn_library.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout.addWidget(self.btn_library)

        self.btn_downloads = QToolButton(self.side_bar)
        self.btn_downloads.setObjectName(u"btn_downloads")
        sizePolicy1.setHeightForWidth(self.btn_downloads.sizePolicy().hasHeightForWidth())
        self.btn_downloads.setSizePolicy(sizePolicy1)
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ObjectRotateRight))
        self.btn_downloads.setIcon(icon4)
        self.btn_downloads.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.btn_downloads.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.verticalLayout.addWidget(self.btn_downloads)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout.addWidget(self.side_bar)

        self.main_entry = QFrame(self.centralwidget)
        self.main_entry.setObjectName(u"main_entry")
        self.main_entry.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_entry.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.main_entry)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.current_view_name = QLabel(self.main_entry)
        self.current_view_name.setObjectName(u"current_view_name")
        font = QFont()
        font.setFamilies([u"Sans"])
        font.setBold(True)
        self.current_view_name.setFont(font)

        self.verticalLayout_3.addWidget(self.current_view_name)

        self.header = QFrame(self.main_entry)
        self.header.setObjectName(u"header")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy2)
        self.header.setMaximumSize(QSize(16777215, 60))
        self.header.setFrameShape(QFrame.Shape.StyledPanel)
        self.header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.header)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.line_search_bar = QLineEdit(self.header)
        self.line_search_bar.setObjectName(u"line_search_bar")

        self.horizontalLayout_2.addWidget(self.line_search_bar)

        self.btn_search_2 = QPushButton(self.header)
        self.btn_search_2.setObjectName(u"btn_search_2")

        self.horizontalLayout_2.addWidget(self.btn_search_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addWidget(self.header)

        self.stackedWidget = QStackedWidget(self.main_entry)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.main_entry)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_toggle.setText("")
        self.btn_search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_library.setText(QCoreApplication.translate("MainWindow", u"Library", None))
        self.btn_downloads.setText(QCoreApplication.translate("MainWindow", u"Downloads", None))
        self.current_view_name.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.line_search_bar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search only Games", None))
        self.btn_search_2.setText(QCoreApplication.translate("MainWindow", u"Search", None))
    # retranslateUi

