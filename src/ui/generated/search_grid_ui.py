# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_grid.ui'
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
from PySide6.QtWidgets import (QApplication, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_SearchGrid(object):
    def setupUi(self, SearchGrid):
        if not SearchGrid.objectName():
            SearchGrid.setObjectName(u"SearchGrid")
        SearchGrid.resize(571, 461)
        self.verticalLayout = QVBoxLayout(SearchGrid)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(SearchGrid)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 551, 441))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
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

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(SearchGrid)

        QMetaObject.connectSlotsByName(SearchGrid)
    # setupUi

    def retranslateUi(self, SearchGrid):
        SearchGrid.setWindowTitle(QCoreApplication.translate("SearchGrid", u"Form", None))
    # retranslateUi

