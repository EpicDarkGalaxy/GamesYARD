# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'home_page.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_home_catalog(object):
    def setupUi(self, home_catalog):
        if not home_catalog.objectName():
            home_catalog.setObjectName(u"home_catalog")
        home_catalog.resize(582, 413)
        self.horizontalLayout = QHBoxLayout(home_catalog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.root_scroll_area = QScrollArea(home_catalog)
        self.root_scroll_area.setObjectName(u"root_scroll_area")
        self.root_scroll_area.setWidgetResizable(True)
        self.root_area_widget = QWidget()
        self.root_area_widget.setObjectName(u"root_area_widget")
        self.root_area_widget.setGeometry(QRect(0, 0, 562, 393))
        self.verticalLayout = QVBoxLayout(self.root_area_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.root_scroll_area.setWidget(self.root_area_widget)

        self.horizontalLayout.addWidget(self.root_scroll_area)


        self.retranslateUi(home_catalog)

        QMetaObject.connectSlotsByName(home_catalog)
    # setupUi

    def retranslateUi(self, home_catalog):
        home_catalog.setWindowTitle(QCoreApplication.translate("home_catalog", u"Form", None))
    # retranslateUi

