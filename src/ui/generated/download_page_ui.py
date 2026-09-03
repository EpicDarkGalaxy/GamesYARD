# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_page.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_download_page(object):
    def setupUi(self, download_page):
        if not download_page.objectName():
            download_page.setObjectName(u"download_page")
        download_page.resize(400, 300)
        self.verticalLayout = QVBoxLayout(download_page)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.download_page_root_container = QFrame(download_page)
        self.download_page_root_container.setObjectName(u"download_page_root_container")
        self.download_page_root_container.setFrameShape(QFrame.Shape.NoFrame)
        self.download_page_root_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.download_page_root_container)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.download_scroll = QScrollArea(self.download_page_root_container)
        self.download_scroll.setObjectName(u"download_scroll")
        self.download_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 392, 292))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.downloads_container = QFrame(self.scrollAreaWidgetContents)
        self.downloads_container.setObjectName(u"downloads_container")
        self.downloads_layout = QVBoxLayout(self.downloads_container)
        self.downloads_layout.setSpacing(6)
        self.downloads_layout.setObjectName(u"downloads_layout")
        self.downloads_layout_2 = QVBoxLayout()
        self.downloads_layout_2.setObjectName(u"downloads_layout_2")

        self.downloads_layout.addLayout(self.downloads_layout_2)


        self.verticalLayout_3.addWidget(self.downloads_container, 0, Qt.AlignmentFlag.AlignTop)

        self.download_scroll.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.download_scroll)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.download_page_root_container)


        self.retranslateUi(download_page)

        QMetaObject.connectSlotsByName(download_page)
    # setupUi

    def retranslateUi(self, download_page):
        download_page.setWindowTitle(QCoreApplication.translate("download_page", u"Form", None))
    # retranslateUi

