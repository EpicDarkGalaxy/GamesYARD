from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QLabel, QPushButton, QWidget

from src.core.utils.log import get_logger
from src.ui.components.download_card import DownloadCard
from src.ui.generated import Ui_downloads_page
from src.ui.components.captcha_dialog import CaptchaBrowserDialog

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
        _ = self.view_model.open_captcha.connect(self._handle_open_captcha)


    @Slot(object)
    def handle_add_card(self, download_view_state):
        self.no_downloads_label.setVisible(False)

        if self._cards.get(download_view_state.id, None):
            logger.info(f"Download Card for id {download_view_state.id} already exists, skipped adding.")
            return # Prevent from creating duplicate card

        card = DownloadCard(
            download_view_state.id,
            download_view_state.name,
            file_size=0,
            resume_supported=download_view_state.resume_supported,
            thumbnail=download_view_state.banner,
        )
        _ = card.cancel_requested.connect(self.view_model.requesting_cancel_download)
        _ = card.pause_requested.connect(self.view_model.requesting_pause_download)
        _ = card.resume_requested.connect(self.view_model.requesting_resume_download)
        self._cards[download_view_state.id] = card
        self.ui.downloads_layout_2.addWidget(card)
        logger.info(f"Added card for download {download_view_state.id}")

    @Slot(object)
    def handle_update_card(self, download_view_state):
        card_id = download_view_state.id
        if not card_id:
            logger.error("Download model has no id")
            return

        card = self._cards.get(card_id, None)
        if card:
            card.update_data(
                downloaded_size=download_view_state.downloaded_size,
                total_size=download_view_state.total_size,
                progress=download_view_state.progress,
                speed=download_view_state.speed,
                eta=download_view_state.eta,
                paused=download_view_state.paused,
                has_finished=download_view_state.has_finished,
                resume_supported=download_view_state.resume_supported
            )

    @Slot(str)
    def handle_remove_card(self, card_id: str):
        if not self._cards:
            self.no_downloads_label.setVisible(True)
            return

        card = self._cards.get(card_id, None)
        if card:
            self.ui.downloads_layout_2.removeWidget(card)
            card.deleteLater()
            del self._cards[card_id]

    @Slot(str)
    def _handle_open_captcha(self, url: str):
        logger.debug(f"Captcha required: url={url}")

        if url:
            dialog = CaptchaBrowserDialog(url, parent=self)
            dialog.show()
            intercepted_link = None
            def on_url_intercepted(url: str):
                nonlocal intercepted_link
                intercepted_link = url
            dialog.download_url_intercepted.connect(on_url_intercepted)
            dialog.accepted.connect(lambda: self._handle_captcha_resolved(intercepted_link))
            dialog.rejected.connect(lambda: self._handle_captcha_resolved(None))
            dialog.finished.connect(lambda: self._handle_captcha_resolved(None))
            self._captcha_dialog = dialog

    @Slot()
    def _handle_captcha_resolved(self, url: str | None):
        logger.debug(f"Captcha resolved: url={url}")
