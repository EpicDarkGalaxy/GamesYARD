# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_page.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_GamePage(object):
    def setupUi(self, GamePage):
        if not GamePage.objectName():
            GamePage.setObjectName(u"GamePage")
        GamePage.resize(484, 783)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GamePage.sizePolicy().hasHeightForWidth())
        GamePage.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(GamePage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scrollArea = QScrollArea(GamePage)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 809))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.btn_back = QPushButton(self.scrollAreaWidgetContents)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy1)

        self.verticalLayout_4.addWidget(self.btn_back)

        self.hero_frame = QFrame(self.scrollAreaWidgetContents)
        self.hero_frame.setObjectName(u"hero_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.hero_frame.sizePolicy().hasHeightForWidth())
        self.hero_frame.setSizePolicy(sizePolicy2)
        self.hero_frame.setMaximumSize(QSize(16777215, 400))
        self.hero_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.hero_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.hero_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.game_poster = QLabel(self.hero_frame)
        self.game_poster.setObjectName(u"game_poster")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.game_poster.sizePolicy().hasHeightForWidth())
        self.game_poster.setSizePolicy(sizePolicy3)
        self.game_poster.setMinimumSize(QSize(0, 0))
        self.game_poster.setMaximumSize(QSize(300, 400))
        self.game_poster.setScaledContents(True)

        self.verticalLayout.addWidget(self.game_poster, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.info_area = QWidget(self.hero_frame)
        self.info_area.setObjectName(u"info_area")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.info_area.sizePolicy().hasHeightForWidth())
        self.info_area.setSizePolicy(sizePolicy4)
        self.verticalLayout_5 = QVBoxLayout(self.info_area)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.meta_info = QGridLayout()
        self.meta_info.setObjectName(u"meta_info")

        self.verticalLayout_5.addLayout(self.meta_info)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.btn_get = QPushButton(self.info_area)
        self.btn_get.setObjectName(u"btn_get")
        sizePolicy1.setHeightForWidth(self.btn_get.sizePolicy().hasHeightForWidth())
        self.btn_get.setSizePolicy(sizePolicy1)
        self.btn_get.setMinimumSize(QSize(0, 0))
        self.btn_get.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.btn_get, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)

        self.providers_container = QFrame(self.info_area)
        self.providers_container.setObjectName(u"providers_container")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.providers_container.sizePolicy().hasHeightForWidth())
        self.providers_container.setSizePolicy(sizePolicy5)
        self.providers_container.setFrameShape(QFrame.Shape.NoFrame)
        self.providers_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.providers_container)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.providers_layout = QVBoxLayout()
        self.providers_layout.setObjectName(u"providers_layout")

        self.verticalLayout_8.addLayout(self.providers_layout)


        self.verticalLayout_2.addWidget(self.providers_container)


        self.verticalLayout_5.addLayout(self.verticalLayout_2)


        self.horizontalLayout_4.addWidget(self.info_area)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.hero_frame)

        self.description_frame = QFrame(self.scrollAreaWidgetContents)
        self.description_frame.setObjectName(u"description_frame")
        sizePolicy.setHeightForWidth(self.description_frame.sizePolicy().hasHeightForWidth())
        self.description_frame.setSizePolicy(sizePolicy)
        self.description_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.description_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.description_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.providers_container_2 = QFrame(self.description_frame)
        self.providers_container_2.setObjectName(u"providers_container_2")
        self.providers_container_2.setFrameShape(QFrame.Shape.NoFrame)
        self.providers_container_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.providers_container_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.providers_container_2)
        self.tabWidget.setObjectName(u"tabWidget")

        self.horizontalLayout_2.addWidget(self.tabWidget)


        self.verticalLayout_3.addWidget(self.providers_container_2)

        self.gallery_container = QFrame(self.description_frame)
        self.gallery_container.setObjectName(u"gallery_container")
        self.gallery_container.setFrameShape(QFrame.Shape.NoFrame)
        self.gallery_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.gallery_container)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.game_screenshots_label = QLabel(self.gallery_container)
        self.game_screenshots_label.setObjectName(u"game_screenshots_label")
        sizePolicy1.setHeightForWidth(self.game_screenshots_label.sizePolicy().hasHeightForWidth())
        self.game_screenshots_label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setBold(True)
        self.game_screenshots_label.setFont(font)

        self.verticalLayout_7.addWidget(self.game_screenshots_label)

        self.gallery_area = QScrollArea(self.gallery_container)
        self.gallery_area.setObjectName(u"gallery_area")
        self.gallery_area.setMinimumSize(QSize(0, 500))
        self.gallery_area.setFrameShape(QFrame.Shape.NoFrame)
        self.gallery_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gallery_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.gallery_area.setWidgetResizable(True)
        self.scroll_widget_container = QWidget()
        self.scroll_widget_container.setObjectName(u"scroll_widget_container")
        self.scroll_widget_container.setGeometry(QRect(0, 0, 386, 500))
        sizePolicy4.setHeightForWidth(self.scroll_widget_container.sizePolicy().hasHeightForWidth())
        self.scroll_widget_container.setSizePolicy(sizePolicy4)
        self.verticalLayout_10 = QVBoxLayout(self.scroll_widget_container)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.gallery_layout = QHBoxLayout()
        self.gallery_layout.setObjectName(u"gallery_layout")

        self.verticalLayout_10.addLayout(self.gallery_layout)

        self.gallery_area.setWidget(self.scroll_widget_container)

        self.verticalLayout_7.addWidget(self.gallery_area)


        self.verticalLayout_3.addWidget(self.gallery_container)

        self.requirements_container = QFrame(self.description_frame)
        self.requirements_container.setObjectName(u"requirements_container")
        self.requirements_container.setFrameShape(QFrame.Shape.Box)
        self.requirements_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.requirements_container)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.sys_req_sec_label = QLabel(self.requirements_container)
        self.sys_req_sec_label.setObjectName(u"sys_req_sec_label")
        sizePolicy1.setHeightForWidth(self.sys_req_sec_label.sizePolicy().hasHeightForWidth())
        self.sys_req_sec_label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Ubuntu"])
        font1.setBold(True)
        font1.setItalic(False)
        self.sys_req_sec_label.setFont(font1)
        self.sys_req_sec_label.setFrameShape(QFrame.Shape.NoFrame)
        self.sys_req_sec_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sys_req_sec_label.setWordWrap(False)

        self.verticalLayout_9.addWidget(self.sys_req_sec_label)

        self.requirements_grid = QGridLayout()
        self.requirements_grid.setObjectName(u"requirements_grid")

        self.verticalLayout_9.addLayout(self.requirements_grid)


        self.verticalLayout_3.addWidget(self.requirements_container)

        self.verticalSpacer_3 = QSpacerItem(20, 39, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.verticalLayout_4.addWidget(self.description_frame)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.retranslateUi(GamePage)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(GamePage)
    # setupUi

    def retranslateUi(self, GamePage):
        GamePage.setWindowTitle(QCoreApplication.translate("GamePage", u"Form", None))
        self.btn_back.setText(QCoreApplication.translate("GamePage", u"Back", None))
        self.game_poster.setText(QCoreApplication.translate("GamePage", u"Poster", None))
        self.btn_get.setText(QCoreApplication.translate("GamePage", u"Get", None))
        self.game_screenshots_label.setText(QCoreApplication.translate("GamePage", u"Screenshots", None))
        self.sys_req_sec_label.setText(QCoreApplication.translate("GamePage", u"System Requirements", None))
    # retranslateUi

