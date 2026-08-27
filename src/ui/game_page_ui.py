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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_GamePage(object):
    def setupUi(self, GamePage):
        if not GamePage.objectName():
            GamePage.setObjectName(u"GamePage")
        GamePage.resize(484, 423)
        self.verticalLayout = QVBoxLayout(GamePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.btn_back = QPushButton(GamePage)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy)

        self.verticalLayout_4.addWidget(self.btn_back)

        self.hero_frame = QFrame(GamePage)
        self.hero_frame.setObjectName(u"hero_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.hero_frame.sizePolicy().hasHeightForWidth())
        self.hero_frame.setSizePolicy(sizePolicy1)
        self.hero_frame.setMaximumSize(QSize(16777215, 400))
        self.hero_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.hero_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.hero_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.game_poster = QLabel(self.hero_frame)
        self.game_poster.setObjectName(u"game_poster")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.game_poster.sizePolicy().hasHeightForWidth())
        self.game_poster.setSizePolicy(sizePolicy2)
        self.game_poster.setMinimumSize(QSize(0, 0))
        self.game_poster.setMaximumSize(QSize(300, 400))
        self.game_poster.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.game_poster)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.info_area = QWidget(self.hero_frame)
        self.info_area.setObjectName(u"info_area")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.info_area.sizePolicy().hasHeightForWidth())
        self.info_area.setSizePolicy(sizePolicy3)
        self.verticalLayout_5 = QVBoxLayout(self.info_area)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.game_title = QLabel(self.info_area)
        self.game_title.setObjectName(u"game_title")
        self.game_title.setWordWrap(False)

        self.verticalLayout_5.addWidget(self.game_title)

        self.game_metadata = QLabel(self.info_area)
        self.game_metadata.setObjectName(u"game_metadata")

        self.verticalLayout_5.addWidget(self.game_metadata)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.btn_get = QPushButton(self.info_area)
        self.btn_get.setObjectName(u"btn_get")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_get.sizePolicy().hasHeightForWidth())
        self.btn_get.setSizePolicy(sizePolicy4)
        self.btn_get.setMinimumSize(QSize(0, 0))
        self.btn_get.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_6.addWidget(self.btn_get)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addWidget(self.info_area)


        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.hero_frame)

        self.description_scroll = QScrollArea(GamePage)
        self.description_scroll.setObjectName(u"description_scroll")
        sizePolicy3.setHeightForWidth(self.description_scroll.sizePolicy().hasHeightForWidth())
        self.description_scroll.setSizePolicy(sizePolicy3)
        self.description_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.description_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 464, 215))
        sizePolicy3.setHeightForWidth(self.scrollAreaWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_4.setSizePolicy(sizePolicy3)
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(20, -1, 20, -1)
        self.label = QLabel(self.scrollAreaWidgetContents_4)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
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
        self.requirements_grid = QGridLayout()
        self.requirements_grid.setObjectName(u"requirements_grid")

        self.verticalLayout_9.addLayout(self.requirements_grid)


        self.verticalLayout_6.addWidget(self.requirements_container)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.description_scroll.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_4.addWidget(self.description_scroll)


        self.verticalLayout.addLayout(self.verticalLayout_4)


        self.retranslateUi(GamePage)

        QMetaObject.connectSlotsByName(GamePage)
    # setupUi

    def retranslateUi(self, GamePage):
        GamePage.setWindowTitle(QCoreApplication.translate("GamePage", u"Form", None))
        self.btn_back.setText(QCoreApplication.translate("GamePage", u"Back", None))
        self.game_poster.setText(QCoreApplication.translate("GamePage", u"Poster", None))
        self.game_title.setText(QCoreApplication.translate("GamePage", u"Title", None))
        self.game_metadata.setText(QCoreApplication.translate("GamePage", u"Metadata", None))
        self.btn_get.setText(QCoreApplication.translate("GamePage", u"Get", None))
        self.label.setText(QCoreApplication.translate("GamePage", u"System Requirements", None))
    # retranslateUi

