from ..windows.game_window import GameWindow
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog
from ..widget import ProviderButton
from ...core.tools import get_logger

logger = get_logger(__name__)


class GamePresenter():
    def __init__(self, view: GameWindow, model):
        self.view = view
        self.model = model
        self.providers = []
        self.downloading_providers = []
        self.bind_signals()

    def bind_signals(self):
        self.view.signals.fetch_btn_clicked.connect(self.on_fetch_btn)


    def on_fetch_btn(self):
        pass

    def on_card_clicked(self, card):
        data = card.get_data
        title = data.title
        thumbnail = data.poster_pixmap
        system_req = data.game_details.system_requirements

        card.thumb_loaded.connect(self.view.set_poster)

        self.view.set_title(title)
        self.view.set_poster(thumbnail)
        self.view.set_description(system_req)
        self.view.update_providers(self.create_provider_list(card))

    def create_provider_list(self, game_card):
        if (not self.game_card.details):
            return

        landing_page_urls = self.model.request_provider_links(game_card.url)
        skip_providers_dict = {provider.landing_page_url: provider for provider in self.model.app_state.download_queue}
        new_providers = []
        for landing_page_url in landing_page_urls:
            if landing_page_url in skip_providers_dict:
                logger.info(f"Provider {landing_page_url} is currently downloading, just readding")
                new_providers.append(skip_providers_dict[landing_page_url])
            else:
                logger.info(f"Adding provider {landing_page_url}")
                name = self.model.request_provider_name(landing_page_url)
                new_providers.append(self.create_provider_button(name, landing_page_url))
        return new_providers


    def create_provider_button(self, name: str, landing_page_url: str):
        provider_btn = ProviderButton(name, landing_page_url, self.on_provider_click, self.on_provider_cancel)

        self.providers.append(provider_btn) # Storing a Reference to keep it alive
        self.ui.download_links_layout.addWidget(provider_btn)
        # self.game_card.details.downloads_links.append(landing_page_url)

    @Slot(str, object)
    def on_provider_cancel(self, landing_page_url: str, provider_btn: ProviderButton):
        self.model.stop_download()
        self.downloading_providers.remove(provider_btn)
        self.model.app_state.is_downloading = False

    @Slot(str, object)
    def on_provider_click(self, landing_page_url, provider_btn: ProviderButton):
        logger.info(f"Clicked Link: {landing_page_url}")
        self.downloading_providers.append(provider_btn)

        suggested_name = self.model.request_filename_from_url(landing_page_url)
        file_path = QFileDialog.getSaveFileName(self.view, "Save Game", suggested_name)
        if (file_path[0] != ""):
            provider_btn.set_downloading_state(True)
            self.model.apps_state.is_downloading = True
            self.model.attempt_download(file_path[0], landing_page_url, provider_btn.update_progress, provider_btn=provider_btn)
