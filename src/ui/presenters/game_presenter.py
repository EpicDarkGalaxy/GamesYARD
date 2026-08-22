from ..windows.game_window import GameWindow
from .presenter_bridge_signals import PRESENTER_BRIDGE_SIGNALS, PresenterBridgeSignals

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog
from ..widget import ProviderButton, GameCard
from ...core.tools import get_logger

logger = get_logger(__name__)

class GamePresenter():
    def __init__(self, view: GameWindow, context):
        self.view = view
        self.context = context
        self.providers = []
        self.bind_signals()

    def bind_signals(self):
        self.view.signals.fetch_btn_clicked.connect(self.on_fetch_btn)

        self.context.signals.opened_card_changed.connect(self.view_card)
        self.context.download_manager.download_finished.connect(self.on_download_finished)

        # PRESENTER_BRIDGE_SIGNALS.show_card.connect(self.on_card_clicked)

    @Slot()
    def on_fetch_btn(self):
        logger.info("Game Window fetch btn clicked")
        if self.context.app_state.opened_card is None:
            return

        providers, skip_providers_dict = self.create_provider_list(self.context.app_state.opened_card)
        self.view.update_providers(providers, skip_providers_dict)

    @Slot(object)
    def view_card(self, card):
        logger.info("card clicked to show")
        self.context.app_state.opened_card = card

        data = card.get_data
        title = data.title
        thumbnail = data.poster_pixmap
        system_req = data.system_requirements

        card.thumb_loaded.connect(self.view.set_poster)

        self.view.set_title(title)
        self.view.set_poster(thumbnail)
        self.view.set_description(system_req)

    def create_provider_list(self, game_card: GameCard):
        data = game_card.get_data
        if (not data):
            return

        landing_page_urls = self.context.request_provider_links(data.url)
        skip_providers_dict = {provider.landing_page_url: provider for provider in self.context.app_state.download_queue}
        new_providers = []
        for landing_page_url in landing_page_urls:
            if landing_page_url in skip_providers_dict:
                logger.info(f"Provider {landing_page_url} is currently downloading, so just readding it")
                new_providers.append(skip_providers_dict[landing_page_url])
            else:
                logger.info(f"Adding provider {landing_page_url}")
                name = self.context.request_provider_name(landing_page_url)
                new_providers.append(self.create_provider_button(name, landing_page_url))
        return new_providers, skip_providers_dict


    def create_provider_button(self, name: str, landing_page_url: str):
        provider_btn = ProviderButton(name, landing_page_url, self.on_provider_click, self.on_provider_cancel)

        self.providers.append(provider_btn) # Storing a Reference to keep it alive
        return provider_btn

    @Slot(str, object)
    def on_provider_cancel(self, landing_page_url: str, provider_btn: ProviderButton):
        self.context.download_manager.stop_download()
        self.context.download_manager.update_download_queue(download_id=provider_btn.get_id, adding=False)
        self.context.download_manager.update_download_state()

    @Slot(str, object)
    def on_provider_click(self, landing_page_url, provider_btn: ProviderButton):
        logger.info(f"Clicked Link: {landing_page_url}")

        suggested_name = self.context.request_filename_from_url(landing_page_url)
        file_path = QFileDialog.getSaveFileName(self.view, "Save Game", suggested_name)
        if (file_path[0] != ""):
            self.context.download_manager.download_progress.connect(provider_btn.update_progress)
            self.context.download_manager.download_finished.connect(self.on_download_finished)
            provider_btn.set_downloading_state(True)
            self.context.download_manager.attempt_download(file_path[0], landing_page_url, provider_btn.get_id)

    @Slot(str)
    def on_download_finished(self, download_id):
        for provider_btn in self.providers:
            if (provider_btn.get_id == download_id):
                provider_btn.set_downloading_state(is_downloading=False, is_downloaded=True)
