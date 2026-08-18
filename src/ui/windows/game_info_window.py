from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QStyleFactory,
    QWidget,
)

from PySide6.QtGui import QPixmap


from ...core.tools import get_logger
from ...ui import Ui_gameinfo
from ..widget.provider_button_widget import ProviderButton

logger = get_logger(__name__)

class GameInfoWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.manager.signals.card_clicked.connect(self.on_game_selected)

        self.setGeometry(100, 100, 600, 600)

        self.providers: list[ProviderButton] = []
        self.downloading_providers: list[ProviderButton] = []  # Providers currently downloading
        self.progress_bars: list[QProgressBar] = []

        self.ui = Ui_gameinfo()
        self.ui.setupUi(self)
        self.ui.fetch_btn.clicked.connect(self.on_fetch_btn)

    @Slot(object)
    def on_game_selected(self, card_widget):
        self.game_card = card_widget.get_data
        title = self.game_card.title
        pixmap = self.game_card.poster_pixmap
        details = self.game_card.details.system_requirements

        card_widget.thumb_loaded.connect(self.set_poster)

        self.set_title(title)
        self.set_poster(pixmap)
        self.set_details(details)
        self.setWindowTitle(f"Game Info - {title}")

    def set_title(self, title: str):
        self.ui.game_name_label.setText(title)

    @Slot(QPixmap)
    def set_poster(self, pixmap):
        print("Loading thumb")
        if (pixmap):
            self.ui.game_poster.setPixmap(pixmap)
        else:
            self.ui.game_poster.setText("NO GAME PHOTO")
            self.ui.game_poster.setAlignment(Qt.AlignCenter)

    def set_details(self, details):
        logger.info("setting details")
        for catg, req in details.items():
            label = QLabel()
            label.setText(f"<b>{catg}</b>: {req}")
            self.ui.game_details_layout.addWidget(label)

    def clear_layout(self, layout, exclude=[]):
        while layout.count():
            item = layout.itemAt(0)
            if item is not None:
                if item.widget() and item.widget() not in exclude:
                    item.widget().deleteLater()
                elif item.layout():
                    self.clear_layout(item.layout())
                    item.layout().deleteLater()
            layout.removeItem(item)

    @Slot()
    def on_fetch_btn(self):
        if (not self.game_card.details):
            return

        # clearing old providers except those currently downloading to avoid duplication
        for provider in self.providers:
            if provider not in self.downloading_providers:
                provider.deleteLater()
        self.clear_layout(self.ui.download_links_layout, exclude=self.downloading_providers)

        landing_page_urls = self.manager.request_provider_links(self.game_card.url)
        for landing_page_url in landing_page_urls:
            if (landing_page_url in [provider.landing_page_url for provider in self.downloading_providers]):
                logger.info(f"Provider {landing_page_url} is currently downloading, skipping")
                continue
            logger.info(f"Adding provider {landing_page_url}")
            name = self.manager.request_provider_name(landing_page_url)
            self.create_provider_button(name, landing_page_url)

    def create_provider_button(self, name: str, landing_page_url: str):
        provider_btn = ProviderButton(name, landing_page_url, self.on_provider_click, self.on_provider_cancel)

        self.providers.append(provider_btn) # Storing a Reference to keep it alive
        self.ui.download_links_layout.addWidget(provider_btn)
        self.game_card.details.downloads_links.append(landing_page_url)

    @Slot(str, object)
    def on_provider_cancel(self, landing_page_url: str, provider_btn: ProviderButton):
        self.manager.stop_download()
        self.downloading_providers.remove(provider_btn)

    @Slot(str, object)
    def on_provider_click(self, landing_page_url, provider_btn: ProviderButton):
        logger.info(f"Clicked Link: {landing_page_url}")
        self.downloading_providers.append(provider_btn)

        suggested_name = self.manager.request_filename_from_url(landing_page_url)
        file_path = QFileDialog.getSaveFileName(self, "Save Game", suggested_name)
        if (file_path[0] != ""):
            provider_btn._is_downloading = True
            self.manager.attempt_download(file_path[0], landing_page_url, provider_btn.update_progress)
