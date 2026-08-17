from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QWidget,
)
from enum import Enum

from ...core import MANAGER, get_logger
from ...ui import Ui_MainWindow
from ...ui.layouts.flow_layout import FlowLayout
from ...ui.widget import LoadMoreButtonWidget
from ...ui.windows.game_info_window import GameInfoWindow

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

        self.setWindowTitle("GamesYARD")
        self.resize(800, 600)

        MANAGER.store_main_window(self)
        self.app_state = MANAGER.app_state

        init_flow_layout(self)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search only games")
        self.search_bar.setClearButtonEnabled(True)

        # Load more button
        # Intializing here since append_to_grid checks if this button exists before
        # removing it
        self.load_more_btn = LoadMoreButtonWidget(MANAGER.on_load_more)

        # Fetch button
        self.fetch_btn = QPushButton()
        self.fetch_btn.setText("Fetch")

        self.bind_signals()

        # Add to toolbar
        self.main_ui.toolBar.addWidget(self.search_bar)
        self.main_ui.toolBar.addWidget(self.fetch_btn)

    def bind_signals(self):
        # Fetch button
        self.fetch_btn.clicked.connect(MANAGER.on_search)

        # Search bar
        self.search_bar.returnPressed.connect(MANAGER.on_search)
        self.search_bar.textChanged.connect(MANAGER.on_search_text_changed)

    @Slot(str, bool)
    def update_fetch_btn(self, msg: str, state:bool):
        self.fetch_btn.setText(msg)
        self.fetch_btn.setEnabled(state)

    @Slot(QWidget)
    def show_window(self, window):
        self.window = window
        window.show()

    @Slot(QWidget)
    def append_to_grid(self, cards):
        logger.info(f"populate_grid called with {len(cards)} games")

        if (self.app_state.clear_grid):
            self.flow_layout.clear_layout()

        if (self.load_more_btn):
            self.flow_layout.removeWidget(self.load_more_btn)
            self.load_more_btn = LoadMoreButtonWidget(MANAGER.on_load_more)

        for card in cards:
            self.flow_layout.addWidget(card)

        self.flow_layout.addWidget(self.load_more_btn)
