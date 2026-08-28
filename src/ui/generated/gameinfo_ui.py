# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gameinfo.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_gameinfo(object):
    def setupUi(self, gameinfo):
        if not gameinfo.objectName():
            gameinfo.setObjectName(u"gameinfo")
        gameinfo.setWindowModality(Qt.WindowModality.NonModal)
        gameinfo.resize(578, 449)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(gameinfo.sizePolicy().hasHeightForWidth())
        gameinfo.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(gameinfo)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutTop = QHBoxLayout()
        self.horizontalLayoutTop.setObjectName(u"horizontalLayoutTop")
        self.horizontalLayoutTop.setContentsMargins(10, 10, 10, 10)
        self.game_poster_layout = QVBoxLayout()
        self.game_poster_layout.setObjectName(u"game_poster_layout")
        self.game_poster_layout.setContentsMargins(10, 10, 10, 10)
        self.game_poster = QLabel(gameinfo)
        self.game_poster.setObjectName(u"game_poster")

        self.game_poster_layout.addWidget(self.game_poster)

        self.fetch_btn = QPushButton(gameinfo)
        self.fetch_btn.setObjectName(u"fetch_btn")
        font = QFont()
        font.setFamilies([u"Bitstream Charter"])
        font.setWeight(QFont.DemiBold)
        font.setItalic(False)
        self.fetch_btn.setFont(font)
        self.fetch_btn.setAutoFillBackground(False)

        self.game_poster_layout.addWidget(self.fetch_btn)


        self.horizontalLayoutTop.addLayout(self.game_poster_layout)

        self.download_info_layout = QVBoxLayout()
        self.download_info_layout.setObjectName(u"download_info_layout")
        self.game_name_label = QLabel(gameinfo)
        self.game_name_label.setObjectName(u"game_name_label")
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(True)
        self.game_name_label.setFont(font1)
        self.game_name_label.setScaledContents(False)
        self.game_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.download_info_layout.addWidget(self.game_name_label)

        self.download_links_area = QScrollArea(gameinfo)
        self.download_links_area.setObjectName(u"download_links_area")
        self.download_links_area.setFrameShape(QFrame.Shape.NoFrame)
        self.download_links_area.setWidgetResizable(True)
        self.download_links_widget = QWidget()
        self.download_links_widget.setObjectName(u"download_links_widget")
        self.download_links_widget.setGeometry(QRect(0, 0, 430, 169))
        self.verticalLayout_5 = QVBoxLayout(self.download_links_widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.download_links_layout = QVBoxLayout()
        self.download_links_layout.setObjectName(u"download_links_layout")
        self.download_links_layout.setContentsMargins(10, 10, 10, 10)

        self.verticalLayout_5.addLayout(self.download_links_layout)

        self.download_links_area.setWidget(self.download_links_widget)

        self.download_info_layout.addWidget(self.download_links_area)


        self.horizontalLayoutTop.addLayout(self.download_info_layout)


        self.verticalLayout.addLayout(self.horizontalLayoutTop)

        self.veroticalLayoutBottom = QVBoxLayout()
        self.veroticalLayoutBottom.setObjectName(u"veroticalLayoutBottom")
        self.veroticalLayoutBottom.setContentsMargins(10, 10, 10, 10)
        self.label = QLabel(gameinfo)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setFamilies([u"Noto Sans Display"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(True)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        self.label.setFont(font2)
        self.label.setScaledContents(True)

        self.veroticalLayoutBottom.addWidget(self.label)

        self.game_details_area = QScrollArea(gameinfo)
        self.game_details_area.setObjectName(u"game_details_area")
        self.game_details_area.setWidgetResizable(True)
        self.game_details_widget = QWidget()
        self.game_details_widget.setObjectName(u"game_details_widget")
        self.game_details_widget.setGeometry(QRect(0, 0, 536, 162))
        self.verticalLayout_6 = QVBoxLayout(self.game_details_widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.game_details_layout = QVBoxLayout()
        self.game_details_layout.setSpacing(3)
        self.game_details_layout.setObjectName(u"game_details_layout")
        self.game_details_layout.setContentsMargins(10, 10, 10, 10)

        self.verticalLayout_6.addLayout(self.game_details_layout)

        self.game_details_area.setWidget(self.game_details_widget)

        self.veroticalLayoutBottom.addWidget(self.game_details_area)


        self.verticalLayout.addLayout(self.veroticalLayoutBottom)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(gameinfo)

        QMetaObject.connectSlotsByName(gameinfo)
    # setupUi

    def retranslateUi(self, gameinfo):
        gameinfo.setWindowTitle(QCoreApplication.translate("gameinfo", u"Form", None))
        self.game_poster.setText(QCoreApplication.translate("gameinfo", u"TextLabel", None))
        self.fetch_btn.setText(QCoreApplication.translate("gameinfo", u"Fetch", None))
        self.game_name_label.setText(QCoreApplication.translate("gameinfo", u"Game Name goes here", None))
        self.label.setText(QCoreApplication.translate("gameinfo", u"System Requirement", None))
    # retranslateUi

