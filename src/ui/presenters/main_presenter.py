from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from ..windows.pages import (
        SearchPageView,
        GamePageView
    )
from .game_page_presenter import GamePagePresenter
from .search_page_presenter import SearchPagePersenter
from ...core.tools.log import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from ...core.app_core import AppCore
    from ...core.models import GameData
    from ..widget import GameCard
    from ..windows.main_window import MainWindow

class MainPresenter:
    def __init__(self, app_core: "AppCore", view: "MainWindow") -> None:
        self.app_core = app_core
        self.view = view
        self.cards = {} # {"ID", GameCard}

        self.search_view = SearchPageView()
        self.search_presenter = SearchPagePersenter(self.search_view, self.app_core)

        self.game_view = GamePageView()
        self.game_presenter = GamePagePresenter(self.game_view, self.app_core)

        self.SEARCH_PAGE_INDEX = self.view.add_page(self.search_view)
        self.GAME_PAGE_INDEX = self.view.add_page(self.game_view)

        self.view.show_page(self.SEARCH_PAGE_INDEX)

        self.bind_signals()


    def bind_signals(self):
        logger.info("MainPresenter: Binding signals")

        # Model Signals
        self.app_core.search_manager.search_completed.connect(self._handle_search_result)
        self.app_core.thumb_manager.thumb_ready.connect(self._handle_thumb_result)

        # View Signals
        self.view.main_ui.btn_search_2.clicked.connect(self.request_search)
        self.view.signals.close.connect(self._on_close) # I want MainPresenter to decide weather to accept or ignore the event

        # View: SearchGrid
        self.search_view.card_created.connect(self.save_card)
        self.search_view.card_clicked.connect(self._handle_card_click)

        # Navigation
        self.game_view.back.connect(lambda: self.view.show_page(self.SEARCH_PAGE_INDEX))

    @Slot("GameCard")
    def save_card(self, card: "GameCard"):
        self.cards[card.id] = card
        self.request_thumb(card.id)

    @Slot()
    def request_search(self):
        query = self.view.main_ui.line_search_bar.text()
        self.app_core.search_manager.search(query=query)


    @Slot(list)
    def _handle_search_result(self, games):
        logger.debug(f"MainPresenter: received games [{len(games)}]")
        self.search_presenter.add_to_grid(games)


    def request_thumb(self, card_id: str):
        card = self.cards.get(card_id)
        if card:
            img_url = card.banner_url
            logger.debug(f"Requesting thumbnail for [{card.title}]")
            self.app_core.thumb_manager.get_thumb(card_id, img_url)
        else:
            logger.warning("Can't request for thumb, Card was not found")

    @Slot(str, bytes) # 1: ID, 2: img data
    def _handle_thumb_result(self, card_id: str, img_data: bytes):
        card = self.cards.get(card_id)
        logger.debug(f"Recieved thumbnail for ID [{card_id}]")

        if card:
            card.thumbnail = img_data
        else:
            logger.warning(f"MainPresenter: Could not set Thumb, Card ID [{card_id}] was not found.")

    @Slot("GameCard")
    def _handle_card_click(self, card: "GameCard"):
        self.game_presenter.load_card(card)
        self.view.show_page(self.GAME_PAGE_INDEX)

    @Slot(object)
    def _on_close(self, event):
        self.app_core.cleanup()
        event.accept()
