from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QPushButton, QWidget

from src.core.utils.log import get_logger
from src.ui.components.download_card import DownloadCard
from src.ui.generated import Ui_downloads_page

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.ui.view_models.download_vm import DownloadViewModel


class DownloadModel:
    def __init__(
        self,
        id: str,
        name: str,
        downloaded_size: int,
        total_size: int,
        progress: int,
        speed: int,
    ):
        self.id: str = id
        self.name: str = name
        self.downloaded_size: int = downloaded_size
        self.total_size: int = total_size
        self.progress: int = progress
        self.speed: int = speed
        self.banner: Optional[object] = None


class DownloadView(QWidget):
    def __init__(self, view_model: "DownloadViewModel"):
        super().__init__()
        self.ui: Ui_downloads_page = Ui_downloads_page()
        self.ui.setupUi(self)

        # Tests
        self.add: QPushButton = QPushButton("Add Download", self)
        _ = self.add.clicked.connect(
            lambda: self.handle_add_card(
                DownloadModel("half_life_2", "Half Life 2", 0, 0, 0, 0)
            )
        )

        self.add_prog: QPushButton = QPushButton("Progress", self)
        _ = self.add_prog.clicked.connect(
            lambda: self.handle_update_card(
                DownloadModel("half_life_2", "Half Life 2", 25000, 100000, 60, 0)
            )
        )

        self.ui.downloads_layout_2.addWidget(self.add)
        self.ui.downloads_layout_2.addWidget(self.add_prog)

        self.view_model: DownloadViewModel = view_model
        self.cards: dict[str, DownloadCard] = {}
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
    def handle_add_card(self, download_model: DownloadModel):
        card = DownloadCard(
            download_model.id,
            download_model.name,
            file_size=0,
            thumbnail=download_model.banner,
        )
        _ = card.cancel.connect(self.view_model.cancel_download)
        self.cards[download_model.id] = card
        self.ui.downloads_layout_2.addWidget(card)

    @Slot(object)
    def handle_update_card(self, download_model: DownloadModel):
        card_id = download_model.id
        if not card_id:
            logger.error("Download model has no id")
            return

        card = self.cards.get(card_id, None)
        if card:
            card.update_data(
                download_model.downloaded_size,
                download_model.total_size,
                download_model.progress,
                download_model.speed,
            )

    @Slot(str)
    def handle_remove_card(self, card_id: str):
        card = self.cards.get(card_id, None)
        if card:
            self.ui.downloads_layout_2.removeWidget(card)
            card.deleteLater()
            del self.cards[card_id]
