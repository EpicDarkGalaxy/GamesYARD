from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSizePolicy, QWidget

from ....core.utils.log import get_logger
from ...layouts import FlowLayout
from ...generated import Ui_SearchGrid
from ...components import GameCard, LoadMoreButton

logger = get_logger(__name__)

class SearchCatalogView(QWidget):
    card_created = Signal(object)
    card_clicked = Signal(object)

    def __init__(self):
        super().__init__()
        self.ui = Ui_SearchGrid()
        self.ui.setupUi(self)

        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.game_grid_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.flow_layout = FlowLayout(self.ui.game_grid_container, margin=20, spacing=20)

    def update_grid(self, games, clear_grid: bool=True):
        logger.info("SearchGridPage: updating search Grid")

        # Clear existing widgets, ensuring we remove all LoadMoreButtons and GameCards
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        for game in games:
            game_card = GameCard(game)
            game_card.clicked.connect(lambda card: self.card_clicked.emit(card))
            self.flow_layout.addWidget(game_card)
            self.card_created.emit(game_card)

        # Add "Load More" button at the end
        load_more_btn = LoadMoreButton()
        self.flow_layout.addWidget(load_more_btn)
