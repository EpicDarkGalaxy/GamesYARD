from typing import TYPE_CHECKING

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QTimer,
    Slot,
)
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QWidget,
)

from ...core import get_logger
from ...ui.generated import Ui_MainWindow
from ...ui.layouts.flow_layout import FlowLayout
from ..ui_signals import MainWindowSignals
from .pages import GameDetailsView, SearchCatalogView

if TYPE_CHECKING:
    from ...core.models import GameData

logger = get_logger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.signals = MainWindowSignals()

        self.setWindowTitle("GamesYARD")
        self.resize(800, 600)

        self.search_grid = SearchCatalogView()
        self.game_page = GameDetailsView()

        # Button-----
        self.main_ui.btn_search_2.clicked.connect(self.search_button)

        # SibeBar
        self.main_ui.btn_toggle.clicked.connect(self.toggle_sidebar)
        self.main_ui.btn_search.clicked.connect(self.toggle_search_bar)

        # SearchBar
        self.main_ui.line_search_bar.returnPressed.connect(self.search_button)


    def search_button(self):
        search_query = self.main_ui.line_search_bar.text()
        self.signals.fetch_btn_clicked.emit(search_query)

    def update_search_button(self, text: str, state: bool):
        self.main_ui.btn_search_2.setText(text)
        self.main_ui.btn_search_2.setEnabled(state)

    def add_page(self, page) -> int:
        return self.main_ui.stackedWidget.addWidget(page)

    def show_page(self, index):
        self.main_ui.stackedWidget.setCurrentIndex(index)

    def toggle_search_bar(self):
        is_expanded = self.main_ui.header.maximumHeight() > 0
        target_height = 0 if is_expanded else 60

        self.anim_max = QPropertyAnimation(self.main_ui.header, b"maximumHeight")
        self.anim_max.setDuration(250)
        self.anim_max.setStartValue(self.main_ui.header.maximumHeight())
        self.anim_max.setEndValue(target_height)
        self.anim_max.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_max.start()

    def toggle_sidebar(self):
        # Determine if expanding or collapsing
        is_expanding = self.main_ui.side_bar.maximumWidth() < 200

        # 1. Swap button styles immediately if collapsing
        if not is_expanding:
            self.set_buttons_icon_only(True)

        # 2. Start width animation
        target_width = 200 if is_expanding else 60

        # Animating maximumWidth
        self.anim_max = QPropertyAnimation(self.main_ui.side_bar, b"maximumWidth")
        self.anim_max.setDuration(250)
        self.anim_max.setStartValue(self.main_ui.side_bar.maximumWidth())
        self.anim_max.setEndValue(target_width)
        self.anim_max.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_max.start()

        # Animating minimumWidth
        self.anim_min = QPropertyAnimation(self.main_ui.side_bar, b"minimumWidth")
        self.anim_min.setDuration(250)
        self.anim_min.setStartValue(self.main_ui.side_bar.minimumWidth())
        self.anim_min.setEndValue(target_width)
        self.anim_min.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_min.start()

        # 3. If expanding, wait for animation to complete before showing text
        if is_expanding:
            QTimer.singleShot(250, lambda: self.set_buttons_icon_only(False))

    def set_buttons_icon_only(self, icon_only: bool):
        # Toggle between icon-only and text-beside-icon
        style = Qt.ToolButtonIconOnly if icon_only else Qt.ToolButtonTextBesideIcon

        # Hook these up to your QToolButton objectNames from Designer
        self.main_ui.btn_search.setToolButtonStyle(style)
        self.main_ui.btn_home.setToolButtonStyle(style)
        self.main_ui.btn_library.setToolButtonStyle(style)
        self.main_ui.btn_downloads.setToolButtonStyle(style)

    def show_confirm_box(self):
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, 'Exit?',
            "A download is currently active. Are you sure you want to exit and cancel it?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        return reply

    def closeEvent(self, event):
        self.signals.close.emit(event)
