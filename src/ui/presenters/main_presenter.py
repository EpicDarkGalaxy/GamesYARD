import uuid

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap

from ...core.manager import Manager
from ...core.tools import get_logger
from ..ui_signals import MainPresenterSignals
from ..widget import GameCard, LoadMoreButton
from ..windows import MainWindow

logger = get_logger(__name__)


class MainPresenter:
    def __init__(self, view: MainWindow, model: Manager):
        self.view: MainWindow = view
        self.view.set_presenter(self)
        self.model = model
        self.signals = MainPresenterSignals()
        self.cards_dict = {}

        self.bind_signals()

    def bind_signals(self):
        self.model.signals.cards_ready.connect(self.on_game_list_ready)
        self.model.signals.update_fetch_btn.connect(self.on_update_fetch_btn)
        self.model.signals.load_more.connect(self.on_load_more)

    def on_fetch_button(self, query: str=""):
        logger.info(f"Requesting games for query: {query}")
        self.model.search(query)

    def on_load_more(self):
        self.model.load_more()

    @Slot(list, bool)
    def on_game_list_ready(self, game_data, clear_grid: bool=False):
        cards = []
        for data in game_data:
            card = GameCard(data, on_click=self.on_card_clicked)
            card.set_id = uuid.uuid4()
            cards.append(card)
            self.cards_dict[card.get_id] = card
            logger.info(f"Adding card: {data.title} with id {card.get_id}")

        load_more_button = LoadMoreButton()
        new_cards = cards + [load_more_button]
        self.view.update_cards(new_cards, clear_grid)

    def on_card_clicked(self, card):
        logger.info(f"Card clicked: {card._data.title} of id {card.get_id}")

        data = card.get_data
        data.details.system_requirements = self.model.request_system_req(data.url)

        self.signals.show_game_info_window.emit()
        self.signals.card_clicked.emit(card)

    def on_update_fetch_btn(self, text: str, state: bool):
        self.view.update_fetch_btn_state(text, state)

    def on_thumbnail_fetched(self, card_id, img_data):
        if card_id not in self.cards_dict and img_data:
            return
        card = self.cards_dict[card_id]
        pixmap = QPixmap.loadFromData(img_data)
        card.set_thumbnail = pixmap
