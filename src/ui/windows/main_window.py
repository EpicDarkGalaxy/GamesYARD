from locale import YESEXPR

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt, Slot, QTimer
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


from typing import TYPE_CHECKING
from ...core import get_logger
from ...ui import Ui_MainWindow
from ...ui.layouts.flow_layout import FlowLayout
from ..ui_signals import MainWindowSignals

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

        self.main_ui.scrollArea.setWidgetResizable(True)
        self.main_ui.game_grid_container.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.flow_layout = FlowLayout(self.main_ui.game_grid_container, margin=20, spacing=20)

        # Button-----
        self.main_ui.btn_search_2.clicked.connect(self.search_button)
        self.main_ui.btn_back.clicked.connect(self.show_grid)

        # SibeBar
        self.main_ui.btn_toggle.clicked.connect(self.toggle_sidebar)
        self.main_ui.btn_search.clicked.connect(self.toggle_search_bar)
        # Button-----

        # SearchBar
        self.main_ui.line_search_bar.returnPressed.connect(self.search_button)

        self.show_grid()

    def search_button(self):
        search_query = self.main_ui.line_search_bar.text()
        self.signals.fetch_btn_clicked.emit(search_query)
        self.show_grid()

    def update_fetch_btn_state(self, text: str, state: bool):
        self.main_ui.btn_search_2.setText(text)
        self.main_ui.btn_search_2.setEnabled(state)

    def update_cards(self, cards, clear_grid: bool):
        logger.info(f"updating grid with {len(cards)} cards")

        # The load more button at the bottom of the grid is removed before adding new cards.
        # This is to have it always at the bottom.
        load_more_button = self.flow_layout.takeAt(self.flow_layout.count() -1)
        if load_more_button is not None:
            load_more_button.widget().deleteLater()

        if (clear_grid):
            self.flow_layout.clear_layout()

        for card in cards:
            self.flow_layout.addWidget(card)

    def show_game(self, game_card):
        data = game_card.get_data
        if data:
            if data.poster_pixmap:
                self.main_ui.game_poster.setPixmap(data.poster_pixmap)
            self.main_ui.game_title.setText(data.title)

        self.display_requirements(data.system_requirements)
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.details_page)

    def display_requirements(self, req_data):
        # 1. Clear existing items from the grid
        layout = self.main_ui.requirments_grid # Your grid object name
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        for row, (label_text, value_text) in enumerate(req_data):
            # Create the UI labels on the fly
            label_widget = QLabel(label_text)
            label_widget.setObjectName("req_label") # Style this in QSS

            value_widget = QLabel(value_text)
            value_widget.setWordWrap(True) # Very important for long text

            layout.addWidget(label_widget, row, 0)
            layout.addWidget(value_widget, row, 1)


    def show_grid(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.grid_page)

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
