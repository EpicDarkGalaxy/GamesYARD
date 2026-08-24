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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(719, 528)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.side_bar = QFrame(self.centralwidget)
        self.side_bar.setObjectName(u"side_bar")
        self.side_bar.setMinimumSize(QSize(200, 0))
        self.side_bar.setMaximumSize(QSize(200, 16777215))
        self.side_bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.side_bar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_search = QPushButton(self.side_bar)
        self.btn_search.setObjectName(u"btn_search")

        self.verticalLayout.addWidget(self.btn_search)

        self.btn_home = QPushButton(self.side_bar)
        self.btn_home.setObjectName(u"btn_home")

        self.verticalLayout.addWidget(self.btn_home)

        self.btn_library = QPushButton(self.side_bar)
        self.btn_library.setObjectName(u"btn_library")

        self.verticalLayout.addWidget(self.btn_library)

        self.btn_downloads = QPushButton(self.side_bar)
        self.btn_downloads.setObjectName(u"btn_downloads")

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
        self.header = QFrame(self.main_entry)
        self.header.setObjectName(u"header")
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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.grid_page = QWidget()
        self.grid_page.setObjectName(u"grid_page")
        sizePolicy.setHeightForWidth(self.grid_page.sizePolicy().hasHeightForWidth())
        self.grid_page.setSizePolicy(sizePolicy)
        self.verticalLayout_10 = QVBoxLayout(self.grid_page)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.scrollArea = QScrollArea(self.grid_page)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 455, 419))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.game_grid_container = QWidget(self.scrollAreaWidgetContents)
        self.game_grid_container.setObjectName(u"game_grid_container")
        sizePolicy.setHeightForWidth(self.game_grid_container.sizePolicy().hasHeightForWidth())
        self.game_grid_container.setSizePolicy(sizePolicy)

        self.verticalLayout_7.addWidget(self.game_grid_container)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_10.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.grid_page)
        self.details_page = QWidget()
        self.details_page.setObjectName(u"details_page")
        sizePolicy.setHeightForWidth(self.details_page.sizePolicy().hasHeightForWidth())
        self.details_page.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.details_page)
        self.verticalLayout_8.setSpacing(20)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_back = QPushButton(self.details_page)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.btn_back)

        self.hero_frame = QFrame(self.details_page)
        self.hero_frame.setObjectName(u"hero_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.hero_frame.sizePolicy().hasHeightForWidth())
        self.hero_frame.setSizePolicy(sizePolicy2)
        self.hero_frame.setMaximumSize(QSize(16777215, 400))
        self.hero_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.hero_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.hero_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.game_poster = QLabel(self.hero_frame)
        self.game_poster.setObjectName(u"game_poster")
        sizePolicy1.setHeightForWidth(self.game_poster.sizePolicy().hasHeightForWidth())
        self.game_poster.setSizePolicy(sizePolicy1)
        self.game_poster.setMinimumSize(QSize(0, 0))
        self.game_poster.setMaximumSize(QSize(300, 400))
        self.game_poster.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.game_poster)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.info_area = QWidget(self.hero_frame)
        self.info_area.setObjectName(u"info_area")
        sizePolicy1.setHeightForWidth(self.info_area.sizePolicy().hasHeightForWidth())
        self.info_area.setSizePolicy(sizePolicy1)
        self.verticalLayout_5 = QVBoxLayout(self.info_area)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.game_title = QLabel(self.info_area)
        self.game_title.setObjectName(u"game_title")

        self.verticalLayout_5.addWidget(self.game_title)

        self.game_metadata = QLabel(self.info_area)
        self.game_metadata.setObjectName(u"game_metadata")

        self.verticalLayout_5.addWidget(self.game_metadata)

        self.btn_get = QPushButton(self.info_area)
        self.btn_get.setObjectName(u"btn_get")

        self.verticalLayout_5.addWidget(self.btn_get)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addWidget(self.info_area)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.hero_frame)

        self.description_scroll = QScrollArea(self.details_page)
        self.description_scroll.setObjectName(u"description_scroll")
        sizePolicy.setHeightForWidth(self.description_scroll.sizePolicy().hasHeightForWidth())
        self.description_scroll.setSizePolicy(sizePolicy)
        self.description_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.description_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 413, 191))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_4.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(20, -1, 20, -1)
        self.label = QLabel(self.scrollAreaWidgetContents_4)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Ubuntu Mono"])
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.Shape.StyledPanel)

        self.verticalLayout_6.addWidget(self.label)

        self.requirements_container = QFrame(self.scrollAreaWidgetContents_4)
        self.requirements_container.setObjectName(u"requirements_container")
        self.requirements_container.setFrameShape(QFrame.Shape.Box)
        self.requirements_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.requirements_container)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.verticalLayout_9.addLayout(self.gridLayout)


        self.verticalLayout_6.addWidget(self.requirements_container)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.description_scroll.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_4.addWidget(self.description_scroll)


        self.verticalLayout_8.addLayout(self.verticalLayout_4)

        self.stackedWidget.addWidget(self.details_page)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.main_entry)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_library.setText(QCoreApplication.translate("MainWindow", u"Library", None))
        self.btn_downloads.setText(QCoreApplication.translate("MainWindow", u"Downloads", None))
        self.line_search_bar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search only Games", None))
        self.btn_search_2.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.btn_back.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.game_poster.setText(QCoreApplication.translate("MainWindow", u"Poster", None))
        self.game_title.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.game_metadata.setText(QCoreApplication.translate("MainWindow", u"Metadata", None))
        self.btn_get.setText(QCoreApplication.translate("MainWindow", u"Get", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"System Requirements", None))
    # retranslateUi

