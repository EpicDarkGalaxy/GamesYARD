from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog

from ...core.tools import get_filename_from_url, get_logger, get_site_name
from ..widget import GameCard, ProviderButton
from ..windows.game_window import GameWindow

if TYPE_CHECKING:
    from ...core.app_core import AppCore
    from PySide6.QtGui import QCloseEvent

logger = get_logger(__name__)

class GamePresenter():
    def __init__(self, view: GameWindow, app_core: "AppCore"):
        self.view = view
        self.app_core = app_core
        self.provider_buttons: dict[str, ProviderButton]= {}
        self.bind_signals()

    def bind_signals(self):
        self.view.signals.fetch_btn_clicked.connect(self.on_fetch_btn)
        self.view.signals.close.connect(self._on_close)

        self.app_core.signals.opened_card_changed.connect(self.view_card)

        self.app_core.download_manager.download_finished.connect(self.on_download_finish)
        self.app_core.download_manager.download_failed.connect(self.on_download_fail)
        self.app_core.download_manager.download_progress.connect(self.on_download_progress)


    @Slot()
    def on_fetch_btn(self):
        logger.debug("Fetch Providers")

        providers, skip_providers = self.create_provider_list(self.app_core.app_state.opened_card)
        self.view.update_providers(providers, skip_providers)

    @Slot(object)
    def view_card(self, card):
        logger.debug("A card was clicked to show")
        if not card:
            logger.warning("A card was clicked to show, but card is None")
            return
        if not card.get_data:
            logger.warning(f"Card data not available for card: {card.get_id}")
            return

        logger.debug(f"Viewing card: {card.get_id}")
        self.app_core.app_state.opened_card = card
        data = card.get_data
        title = data.title
        thumbnail = data.poster_pixmap
        system_req = data.system_requirements

        card.thumb_loaded.connect(self.view.set_poster)

        self.view.set_title(title)
        self.view.set_poster(thumbnail)
        self.view.set_description(system_req)

    def create_provider_list(self, card: GameCard) -> tuple[list[ProviderButton], list[ProviderButton]]:
        logger.debug(f"Create provider list for card: {card.get_id}")

        data = card.get_data
        provider_urls = self.app_core.search_manager.get_host_urls(data.url)
        if not provider_urls:
            logger.warning("Provider URLs is Empty")
            return [], {}

        # [skip_providers] We don't want to Recreate Providers that are downloading
        downloading_ids = self._get_downloading_providers()
        logger.debug(f"Downloading Provider: [{len(downloading_ids)}]")
        skip_providers: list[ProviderButton] = []
        new_providers: list[ProviderButton] = []

        for url in provider_urls:
            name = get_site_name(url)
            # Find if this provider was already created and is in the download queue
            found_id = next((pid for pid, btn in self.provider_buttons.items()
                             if btn.provider_url == url and pid in downloading_ids), None)

            if found_id:
                logger.debug(f"Provider {url} is currently downloading, so just readding it")
                skip_providers.append(self.provider_buttons[found_id])
            else:
                logger.info(f"Adding provider {url}")
                new_providers.append(self.create_provider_button(name, url))

        logger.debug(f"Returning providers: new=[{len(new_providers)}], old=[{len(skip_providers)}]")
        return new_providers, skip_providers

    def _get_downloading_providers(self) -> list[str]:
        dl_providers_id = []
        for id in self.app_core.download_manager.download_queue.keys():
            if id in self.provider_buttons.keys():
                dl_providers_id.append(id)
        return dl_providers_id

    def create_provider_button(self, name: str, url: str):
        logger.debug(f"GamePresenter: create_provider_button called with name={name}, url={url}")

        metadata = self._get_provider_metadata(url)
        if metadata:
            btn = ProviderButton(metadata["name"], metadata["url"])
            btn.set_state(
                is_downloading=metadata["is_downloading"],
                is_downloaded=metadata["is_downloaded"],
                failed=metadata["has_failed"]
            )
            btn.set_id = metadata["id"]
        else:
            btn = ProviderButton(name, url)

        btn.download_requested.connect(self.on_provider_click)
        btn.cancel_requested.connect(self.on_provider_cancel)

        self.provider_buttons[btn.get_id] = btn
        return btn

    @Slot(str, str)
    def on_provider_cancel(self, provider_url: str="", provider_id: str=""):
        btn = self.provider_buttons.get(provider_id)
        if not btn:
            logger.warning(f"Provider button not found for id: {provider_id}")
            return

        self.app_core.download_manager.stop_download(provider_id)
        self.app_core.download_manager.download_progress.disconnect(btn.update_progress)

    @Slot(str, object)
    def on_provider_click(self, provider_url: str, provider_id: str):
        logger.debug(f"Clicked Provider: {provider_url}")

        btn = self.provider_buttons.get(provider_id)
        if not btn:
            logger.warning(f"Provider button not found for id: {provider_id}")
            return

        suggested_name = get_filename_from_url(provider_url)
        file_path = QFileDialog.getSaveFileName(self.view, "Save Game", suggested_name)
        if (file_path[0] != ""):
            btn.set_state(is_downloading=True)
            self.app_core.download_manager.queue_download(file_path[0], provider_url, provider_id)

    @Slot(str, int)
    def on_download_progress(self, provider_id: str="", progress: int=0):
        btn = self.provider_buttons.get(provider_id)
        if (btn):
            btn.update_progress(progress)

    # ------I will refactor it later------
    @Slot(str)
    def on_download_finish(self, download_id: str):
        logger.debug(f"Download Finished for provider: {download_id}")
        btn = self.provider_buttons.get(download_id)
        if not btn:
            logger.warning(f"Provider not found for download id: {download_id}")
            return
        btn.set_state(is_downloaded=True)

    @Slot(str)
    def on_download_fail(self, download_id: str):
        logger.debug(f"Download failed for provider: {download_id}")
        btn = self.provider_buttons.get(download_id)
        if not btn:
            logger.warning(f"Provider not found for download id: {download_id}")
            return
        btn.set_state(failed=True)
    # ------I will refactor it later------

    @Slot(object)
    def _on_close(self, event: "QCloseEvent"):
        if self._store_provider_metadata():
            event.accept()
        else:
            event.ignore()

    def _store_provider_metadata(self) -> bool:
        downloading_ids = self._get_downloading_providers()
        if not downloading_ids:
            logger.debug("No active downloads to preserve.")
            return True

        for pid in downloading_ids:
            btn = self.provider_buttons.get(pid)
            if btn:
                logger.debug(f"Storing metadata and preserving provider during close: {btn.provider_url}")
                is_downloading, is_downloaded, has_failed = btn.get_state
                self.app_core.download_manager.store_download_metadata(
                    pid,
                    {
                        "name": btn.provider_name,
                        "id": btn.get_id,
                        "url": btn.provider_url,
                        "is_downloading": is_downloading,
                        "is_downloaded": is_downloaded,
                        "has_failed": has_failed,
                    },
                )
                btn.setParent(None)
        return True

    def _get_provider_metadata(self, provider_url: str=""):
        return self.app_core.download_manager.get_download_metadata(provider_url)
