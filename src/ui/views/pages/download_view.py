from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Slot, Qt
from src.ui.generated.download_page_ui import Ui_download_page
from src.ui.components import DownloadCard
from src.core.utils.log import get_logger
from typing import TYPE_CHECKING


logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.ui.view_models.download_vm import DownloadViewModel

class DownloadView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.ui = Ui_download_page()
        self.ui.setupUi(self)
        self.view_model: DownloadViewModel = view_model
        self.cards = {}

    def initialize(self):
        self.no_downloads_label = QLabel("Cause' I love the adrenaline in my veins!", self)
        self.no_downloads_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 14px;
                font-style: italic;
                margin-top: 20px;
            }
        """)
        self.no_downloads_label.setAlignment(Qt.AlignCenter)
        self.ui.downloads_layout_2.addWidget(self.no_downloads_label)
        self.bind_signals()

    def bind_signals(self):
        self.view_model.update_view.connect(self.update_download_card)
        self.view_model.add_card.connect(self.add_download_card)

    @Slot(str, str)
    def add_download_card(self, id: str, name: str):
        if hasattr(self, 'no_downloads_label') and self.no_downloads_label:
            self.no_downloads_label.setParent(None)
            self.no_downloads_label = None

        logger.info(f"Adding download card: {id}")
        card = DownloadCard(id, name, 0)
        self.cards[card.id] = card
        self.ui.downloads_layout_2.addWidget(card)

    @Slot(object)
    def update_download_card(self, download_model):
        card_id = download_model.id
        if not card_id:
            logger.error("Download model has no id")
            return

        card = self.cards.get(card_id, None)
        if card:
            card.update_data(download_model.downloaded_size, download_model.total_size, download_model.progress, download_model.speed)
