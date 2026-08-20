from uuid import uuid4

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap

from ...core.manager import Manager
from ...core.tools import get_logger
from ..ui_signals import MainPresenterSignals
from ..widget import GameCard, LoadMoreButton
from ..windows import MainWindow
from .presenter_bridge_signals import PRESENTER_BRIDGE_SIGNALS

logger = get_logger(__name__)


class MainPresenter:
    def __init__(self, view: MainWindow, model: Manager, window_controller=None):
        self.view: MainWindow = view
        self.model = model
        self.signals = MainPresenterSignals()
        self.window_controller = window_controller
        self.cards_dict = {}

        self.bind_signals()

    def bind_signals(self):
        self.model.signals.cards_ready.connect(self.on_game_list_ready)
        self.model.signals.update_fetch_btn.connect(self.on_update_fetch_btn)
        self.model.signals.load_more.connect(self.on_load_more)
        self.model.signals.thumb_fetched.connect(self.on_thumbnail_fetched)

        self.view.signals.fetch_btn_clicked.connect(self.on_fetch_button)

    @Slot(str)
    def on_fetch_button(self, query: str=""):
        logger.info(f"Requesting games for query: {query}")
        self.model.search(query)

    @Slot()
    def on_load_more(self):
        self.model.load_more()

    @Slot(list, bool)
    def on_game_list_ready(self, game_data, clear_grid: bool=False):
        cards = []
        for data in game_data:
            card = GameCard(data, on_click=self.on_card_clicked)
            card.set_id = str(uuid4())
            cards.append(card)
            self.cards_dict[card.get_id] = card

            self.model.request_thumbnail(card.get_id, data.poster_url)
            logger.info(f"Adding card: {data.title} with id {card.get_id}")

        load_more_button = LoadMoreButton(self.on_load_more)
        new_cards = cards + [load_more_button]
        self.view.update_cards(new_cards, clear_grid)

    @Slot(GameCard)
    def on_card_clicked(self, card):
        logger.info(f"Card clicked: {card._data.title} of id {card.get_id}")

        data = card.get_data
        data.details.system_requirements = self.model.request_system_req(data.url)

        self.window_controller.show_GameInfoWindow()
        PRESENTER_BRIDGE_SIGNALS.card_clicked_to_show.emit(card)

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
