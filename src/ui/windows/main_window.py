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
        self.setWindowTitle("4fnet FrontEnd")
        self.resize(500, 400)

        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        self.manager = MANAGER
        self.manager.store_main_window(self)
        self.app_state = self.manager.app_state

        init_flow_layout(self)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search only games")
        self.search_bar.setClearButtonEnabled(True)

        # Load more button
        # Intializing here since append_to_grid checks if this button exists before
        # removing it then recreating it again
        self.load_more_btn = LoadMoreButtonWidget(self.manager.on_load_more)

        # Fetch button
        self.fetch_btn = QPushButton()
        self.fetch_btn.setText("Fetch")

        self.connect_signals()

        # Add to toolbar
        self.main_ui.toolBar.addWidget(self.search_bar)
        self.main_ui.toolBar.addWidget(self.fetch_btn)

    def connect_signals(self):
        # Fetch button
        self.fetch_btn.clicked.connect(self.manager.on_search)

        # Search bar
        self.search_bar.returnPressed.connect(self.manager.on_search)
        self.search_bar.textChanged.connect(self.manager.on_search_text_changed)

        self.manager.game_info_signals.request_show_window.connect(self.show_window)

    def update_fetch_btn(self, msg: str, state:bool):
        self.fetch_btn.setText(msg)
        self.fetch_btn.setEnabled(state)

    def show_window(self, window):
        self.window = window
        window.show()

    def append_to_grid(self, cards):
        # logger.info(f"populate_grid called with {len(cards)} games")

        if (self.app_state.clear_grid):
            self.flow_layout.clear_layout()

        if (self.load_more_btn):
            self.flow_layout.removeWidget(self.load_more_btn)
            self.load_more_btn = LoadMoreButtonWidget(self.manager.on_load_more)

        for card in cards:
            self.flow_layout.addWidget(card)

        self.flow_layout.addWidget(self.load_more_btn)

    def set_thumbnail(self, pixmap: QPixmap, target):
        logger.info(f"setting thumbnail for {target._card.title}")

        if target:
            logger.info(f"storing thumbnail for {target._card.title} in its CardData")

            # Instead of fixed size, using 'KeepAspectRatio'
            scaled_pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            target.card_thumbnail.setPixmap(scaled_pixmap)

            # Store the data model
            target._card.poster_pixmap = pixmap

            # Update the UI
            target.card_thumbnail.setPixmap(scaled_pixmap)
