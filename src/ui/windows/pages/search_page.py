from PySide6.QtWidgets  import QWidget, QSizePolicy
from PySide6.QtCore import Signal
from ...layouts import FlowLayout
from ....core.tools.log import get_logger
from ...search_grid_ui import Ui_SearchGrid
from ...widget import GameCard

logger = get_logger(__name__)

class SearchPageView(QWidget):
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

        if clear_grid:
            while self.flow_layout.count():
                item = self.flow_layout.takeAt(0)
                if item and item.widget():
                    item.widget().deleteLater()
        else:
            item = self.flow_layout.takeAt(-1)
            if item and item.widget():
                item.widget().deleteLater()

        for game in games:
            game_card = GameCard(game)
            game_card.clicked.connect(lambda card: self.card_clicked.emit(card))
            self.flow_layout.addWidget(game_card)
            self.card_created.emit(game_card)

        # Add "Load More" button at the end
        from PySide6.QtWidgets import QPushButton
        load_more_btn = QPushButton("Load More")
        self.flow_layout.addWidget(load_more_btn)
