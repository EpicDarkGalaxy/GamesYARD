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

from src.core.utils.log import get_logger
from src.ui.generated import Ui_MainWindow

if TYPE_CHECKING:
<<<<<<< HEAD
    from src.ui.navigator import Navigator
=======
    from ...core.models import GameData
    from ..navigator import Navigator
>>>>>>> 49411a3e9ffa7ace8a740fca7c33696c699c18bc

logger = get_logger(__name__)

class MainView(QMainWindow):
    def __init__(self, view_model, navigator: "Navigator"):
        super().__init__()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.setWindowTitle("GamesYARD")
        self.resize(800, 600)

        self.view_model = view_model
        self.navigator = navigator
<<<<<<< HEAD
=======
        self.signals = MainWindowSignals()
>>>>>>> 49411a3e9ffa7ace8a740fca7c33696c699c18bc

        self.bind_signals()
        self.navigator.go_to("search")

    def bind_signals(self):
        # MainView -> View Model
        self.main_ui.btn_search_2.clicked.connect(
            lambda: self.view_model.request_search(self.main_ui.line_search_bar.text())
        )

        # MainView <- View Model
        self.view_model.search_state_changed.connect(self.update_search_button)

        # Navigator
        self.navigator.request_page_change.connect(self._perform_switch)

        # SibeBar
        self.main_ui.btn_toggle.clicked.connect(self._toggle_sidebar)
        self.main_ui.btn_search.clicked.connect(self._toggle_search_bar)

        # SearchBar
        self.main_ui.line_search_bar.returnPressed.connect(
            lambda: self.view_model.request_search(self.main_ui.line_search_bar.text())
        )

    def init_views(self, search_view, details_view):
        logger.info("Initializing search and details views")

        self.add_page("search", search_view)
        self.add_page("details", details_view)
        self.navigator.go_to("search") # Set Default viewe to search catalog

    def add_page(self, key: str, page: QWidget):
        logger.info(f"Adding page '{key}' to stacked widget: {page.__class__.__name__}")
        self.navigator.register_page(key, page)
        self.main_ui.stackedWidget.addWidget(page)

    @Slot(str)
    def _perform_switch(self, key: str):
        logger.info(f"Attempting to switch to page: {key}")
        widget = self.navigator._page_registry.get(key)
        if widget:
            logger.info(f"Now at page: [{key}]")
            self.main_ui.stackedWidget.setCurrentWidget(widget)
        else:
            logger.warning(f"Failed to find page with key: {key}")

    @Slot(str, bool)
    def update_search_button(self, text: str, state: bool):
        self.main_ui.btn_search_2.setText(text)
        self.main_ui.btn_search_2.setEnabled(state)

    def _toggle_search_bar(self):
        is_expanded = self.main_ui.header.maximumHeight() > 0
        target_height = 0 if is_expanded else 60

        self.anim_max = QPropertyAnimation(self.main_ui.header, b"maximumHeight")
        self.anim_max.setDuration(250)
        self.anim_max.setStartValue(self.main_ui.header.maximumHeight())
        self.anim_max.setEndValue(target_height)
        self.anim_max.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_max.start()

    def _toggle_sidebar(self):
        # Determine if expanding or collapsing
        is_expanding = self.main_ui.side_bar.maximumWidth() < 200

        # 1. Swap button styles immediately if collapsing
        if not is_expanding:
            self._set_buttons_icon_only(True)

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
            QTimer.singleShot(250, lambda: self._set_buttons_icon_only(False))

    def _set_buttons_icon_only(self, icon_only: bool):
        # Toggle between icon-only and text-beside-icon
        style = Qt.ToolButtonIconOnly if icon_only else Qt.ToolButtonTextBesideIcon

        # Hook these up to your QToolButton objectNames from Designer
        self.main_ui.btn_search.setToolButtonStyle(style)
        self.main_ui.btn_home.setToolButtonStyle(style)
        self.main_ui.btn_library.setToolButtonStyle(style)
        self.main_ui.btn_downloads.setToolButtonStyle(style)

    @Slot()
    def show_confirm_box(self):
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, 'Exit?',
            "A download is currently active. Are you sure you want to exit and cancel it?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        return reply

    def closeEvent(self, event):
        self.view_model._on_close(event)
