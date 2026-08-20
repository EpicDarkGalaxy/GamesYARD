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

        init_flow_layout(self)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search only games")
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.returnPressed.connect(self.fetch_button)

        # Fetch button
        self.fetch_btn = QPushButton()
        self.fetch_btn.setText("Fetch")
        self.fetch_btn.clicked.connect(self.fetch_button)

        # Add to toolbar
        self.main_ui.toolBar.addWidget(self.search_bar)
        self.main_ui.toolBar.addWidget(self.fetch_btn)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def fetch_button(self):
        text = self.search_bar.text()
        self.presenter.on_fetch_button(text)

    def update_fetch_btn_state(self, text: str, state: bool):
        self.fetch_btn.setText(text)
        self.fetch_btn.setEnabled(state)

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

    # def closeEvent(self, event):
    #     # Check if a download is active
    #     if hasattr(self.manager, 'app_state') and self.manager.app_state.is_downloading:
    #         from PySide6.QtWidgets import QMessageBox
    #         reply = QMessageBox.question(
    #             self, 'Exit?',
    #             "A download is currently active. Are you sure you want to exit and cancel it?",
    #             QMessageBox.Yes | QMessageBox.No, QMessageBox.No
    #         )

    #         if reply == QMessageBox.No:
    #             event.ignore() # Cancel the close event!
    #             return

    #     # If no download or they clicked Yes, proceed with cleanup
    #     logger.info("Cleaning up and exiting...")
    #     self.manager.cleanup()
    #     event.accept()
