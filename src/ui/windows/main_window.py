from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QWidget,
    QSizePolicy,
    QLabel
)
from ..ui_signals import MainWindowSignals
from ...core import get_logger
from ...ui import Ui_MainWindow
from ...ui.layouts.flow_layout import FlowLayout

logger = get_logger(__name__)

def init_flow_layout(self):
    self.area = QScrollArea(self.main_ui.centralwidget)
    self.area.setWidgetResizable(True)
    self.area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.area.setFrameShape(QFrame.NoFrame)

    # 1. Create the container widget
    self.container = QWidget()

    # 2. Attach the FlowLayout DIRECTLY to this container
    self.flow_layout = FlowLayout(self.container, margin=20, spacing=20)

    # Let's simplify:
    self.area.setWidget(self.container)
    self.setCentralWidget(self.area)

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

        # Buttons
        self.main_ui.btn_search_2.clicked.connect(self.search_button)
        self.main_ui.btn_back.clicked.connect(self.show_grid)

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

    def show_game_details(self, game_card):
        data = game_card.get_data
        if data:
            self.main_ui.game_poster.setPixmap(data.poster_pixmap)
            self.main_ui.game_title.setText(data.title)

        logger.info("setting details")
        for catg, req in data.system_requirements.items():
            label = QLabel()
            label.setText(f"<b>{catg}</b>: {req}")
            self.main_ui.verticalLayout_9.addWidget(label)

            self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.details_page)

    def show_grid(self):
        self.main_ui.stackedWidget.setCurrentWidget(self.main_ui.grid_page)

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
