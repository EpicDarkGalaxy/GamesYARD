from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox
from typing import TYPE_CHECKING

from ...core.tools import get_logger
from ..ui_signals import MainPresenterSignals
from ..widget import GameCard, LoadMoreButton
from ..windows import MainWindow
from .presenter_bridge_signals import PRESENTER_BRIDGE_SIGNALS

logger = get_logger(__name__)

if TYPE_CHECKING:
    from ...core.app_core import AppCore
    from ...core.models import GameData


class MainPresenter:
    def __init__(self, view: MainWindow, app_core: "AppCore", window_controller=None):
        self.view: MainWindow = view
        self.app_core = app_core
        self.signals = MainPresenterSignals()
        self.window_controller = window_controller
        self.cards_dict = {}

        self.bind_signals()

    def bind_signals(self):
        self.app_core.search_manager.search_completed.connect(self.on_game_list_ready)
        self.app_core.search_manager.search_state_changed.connect(self.on_update_fetch_btn)
        self.app_core.thumbnail_manager.thumbnail_ready.connect(self.on_thumbnail_fetched)

        self.view.signals.fetch_btn_clicked.connect(self.on_fetch_button)
        self.view.signals.close.connect(self.on_close)

    @Slot(str)
    def on_fetch_button(self, query: str=""):
        logger.info(f"Requesting games for query: {query}")
        self.app_core.search_manager.search(query)

    @Slot()
    def on_load_more(self):
        self.app_core.search_manager.load_more()

    @Slot(list, bool)
    def on_game_list_ready(self, games_data: list["GameData"], clear_grid: bool):
        logger.info(f"Received {len(games_data)} games ({clear_grid=})")

        cards = []
        for data in games_data:
            card = GameCard(data, on_click=self.on_card_clicked)
            cards.append(card)
            self.cards_dict[card.get_id] = card

            self.app_core.thumbnail_manager.request_thumbnail(card.get_id, data.poster_url)
            logger.info(f"Adding card: {data.title} with id {card.get_id}")

        load_more_button = LoadMoreButton(self.on_load_more)
        new_cards = cards + [load_more_button]
        self.view.update_cards(new_cards, clear_grid)

    @Slot(GameCard)
    def on_card_clicked(self, card):
        logger.info(f"Card clicked: {card._data.title} of id {card.get_id}")

        data = card.get_data
        data.system_requirements = self.app_core.request_system_req(data.url)

        self.window_controller.show_GameInfoWindow()
        self.app_core.app_state.set_opened_card = card


    @Slot(str, bool)
    def on_update_fetch_btn(self, text: str, state: bool):
        self.view.update_fetch_btn_state(text, state)

    @Slot(str, bytes)
    def on_thumbnail_fetched(self, card_id: str, img_data: bytes):
        if card_id not in self.cards_dict.keys():
            return

        pixmap = QPixmap()
        card = self.cards_dict[card_id]
        if img_data and card:
            pixmap.loadFromData(img_data)
            if pixmap.isNull():
                logger.warning(f"Failed to load thumbnail for card {card.get_data.title}")
                return
            logger.info(f"Setting thumbnail for card {card.get_data.title}")
            card.set_thumbnail = pixmap
        else:
            logger.warning(f"No image data or card found for card {card.get_data.title}")

    @Slot(object)
    def on_close(self, event):
        if self.app_core.app_state.is_downloading:
            reply = self.view.show_confirm_box()
            logger.info(f"Close reply: {reply}")
            if reply == QMessageBox.No:
                logger.info("User cancelled close")
                event.ignore()
                return
        self.app_core.cleanup(event)
