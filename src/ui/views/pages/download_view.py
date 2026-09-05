from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QPushButton, QWidget

from src.core.utils.log import get_logger
from src.ui.components.download_card import DownloadCard
from src.ui.generated import Ui_downloads_page

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.ui.view_models.download_vm import DownloadViewModel

class DownloadView(QWidget):
    def __init__(self, view_model: "DownloadViewModel"):
        super().__init__()
        self.ui: Ui_downloads_page = Ui_downloads_page()
        self.ui.setupUi(self)
        self.view_model: DownloadViewModel = view_model
        self._cards: dict[str, DownloadCard] = {}
        self.no_downloads_label: QLabel

    def initialize(self):
        self.no_downloads_label = QLabel(
            "Cause' I love the ANDRENALINE in my veins!", self
        )
        self.no_downloads_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 14px;
                font-style: italic;
                margin-top: 20px;
            }
        """)
        self.no_downloads_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.downloads_layout_2.addWidget(self.no_downloads_label)
        self.bind_signals()

    def bind_signals(self):
        _ = self.view_model.update_view.connect(self.handle_update_card)
        _ = self.view_model.add_card.connect(self.handle_add_card)
        _ = self.view_model.remove_card.connect(self.handle_remove_card)

    @Slot(object)
    def handle_add_card(self, download_model):
        if self._cards.get(download_model.id, None):
            logger.info(f"Download Card for id {download_model.id} already exists, skipped adding.")
            return # Prevent from creating duplicate card

        card = DownloadCard(
            download_model.id,
            download_model.name,
            file_size=0,
            resume_supported=download_model.resume_supported,
            thumbnail=download_model.banner,
        )
        _ = card.cancel.connect(self.view_model.cancel_download)
        _ = card.pause.connect(self.view_model.pause_download)
        _ = card.resume.connect(self.view_model.resume_download)
        self._cards[download_model.id] = card
        self.ui.downloads_layout_2.addWidget(card)
        logger.info(f"Added card for download {download_model.id}")

    @Slot(object)
    def handle_update_card(self, download_model):
        card_id = download_model.id
        if not card_id:
            logger.error("Download model has no id")
            return

        card = self._cards.get(card_id, None)
        if card:
            card.update_data(
                download_model.downloaded_size,
                download_model.total_size,
                download_model.progress,
                download_model.speed,
                download_model.paused,
                download_model.resume_supported
            )

    @Slot(str)
    def handle_remove_card(self, card_id: str):
        card = self._cards.get(card_id, None)
        if card:
            self.ui.downloads_layout_2.removeWidget(card)
            card.deleteLater()
            del self._cards[card_id]
