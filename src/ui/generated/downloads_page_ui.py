# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'downloads_page.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_downloads_page(object):
    def setupUi(self, downloads_page):
        if not downloads_page.objectName():
            downloads_page.setObjectName(u"downloads_page")
        downloads_page.resize(400, 300)
        self.verticalLayout = QVBoxLayout(downloads_page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.download_page_root_container = QFrame(downloads_page)
        self.download_page_root_container.setObjectName(u"download_page_root_container")
        self.download_page_root_container.setFrameShape(QFrame.Shape.NoFrame)
        self.download_page_root_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.download_page_root_container)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.download_scroll = QScrollArea(self.download_page_root_container)
        self.download_scroll.setObjectName(u"download_scroll")
        self.download_scroll.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 376, 276))
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

        self.verticalLayout_4.addWidget(self.download_scroll)


        self.verticalLayout_2.addLayout(self.verticalLayout_4)


        self.verticalLayout.addWidget(self.download_page_root_container)


        self.retranslateUi(downloads_page)

        QMetaObject.connectSlotsByName(downloads_page)
    # setupUi

    def retranslateUi(self, downloads_page):
        downloads_page.setWindowTitle(QCoreApplication.translate("downloads_page", u"Form", None))
    # retranslateUi

