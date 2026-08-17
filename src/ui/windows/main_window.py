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

from ...core import get_logger
from ...ui import Ui_MainWindow
from ...ui.layouts.flow_layout import FlowLayout
from ...ui.widget import LoadMoreButtonWidget

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
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.setWindowTitle("GamesYARD")
        self.resize(800, 600)

        self.app_state = self.manager.app_state

        init_flow_layout(self)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search only games")
        self.search_bar.setClearButtonEnabled(True)

        # Load more button
        # Intializing here since append_to_grid checks if this button exists before
        # removing it
        self.load_more_btn = LoadMoreButtonWidget(self.manager.on_load_more)

        # Fetch button
        self.fetch_btn = QPushButton()
        self.fetch_btn.setText("Fetch")


        # Add to toolbar
        self.main_ui.toolBar.addWidget(self.search_bar)
        self.main_ui.toolBar.addWidget(self.fetch_btn)

        self.bind_signals()

    def bind_signals(self):
        # Manager
        self.manager.signals.cards_ready.connect(self.append_to_grid)
        self.manager.signals.update_fetch_btn.connect(self.update_fetch_btn)

        # Fetch button
        self.fetch_btn.clicked.connect(self.manager.on_search)

        # Search bar
        self.search_bar.returnPressed.connect(self.manager.on_search)
        self.search_bar.textChanged.connect(self.manager.on_search_text_changed)

    @Slot(str, bool)
    def update_fetch_btn(self, msg: str, state:bool):
        self.fetch_btn.setText(msg)
        self.fetch_btn.setEnabled(state)

    @Slot(list)
    def append_to_grid(self, cards):
        logger.info(f"populate_grid called with {len(cards)} games")

        if (self.app_state.clear_grid):
            self.flow_layout.clear_layout()

        if (self.load_more_btn):
            self.flow_layout.removeWidget(self.load_more_btn)
            self.load_more_btn = LoadMoreButtonWidget(self.manager.on_load_more)

        for card in cards:
            self.flow_layout.addWidget(card)

        self.flow_layout.addWidget(self.load_more_btn)
