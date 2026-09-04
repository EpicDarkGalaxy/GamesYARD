from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListView,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from src.core.utils.log import get_logger
from src.ui.components.hoverable_list_view import HoverableListView
from src.ui.delegates.game_card_delegate import GameCardDelegate
from src.ui.generated import Ui_home_catalog
from src.ui.models.game_list_model import GameListModel

logger = get_logger(__name__)

class HomeCatalogView(QWidget):
    def __init__(self, view_model) -> None:
        super().__init__()
        self.ui = Ui_home_catalog()
        self.ui.setupUi(self)
        self.view_model = view_model
        self.ui.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignTop) # Align everything to the top

        # Store models so we can update them when data arrives
        self.models = {}

    def initialize(self):
        self.bind_signals()

    def bind_signals(self):
        self.view_model.set_heros.connect(self.set_heros)
        self.view_model.set_trending.connect(self.set_trending)
        self.view_model.set_newest.connect(self.set_newest)
        self.view_model.set_best_rated.connect(self.set_best_rated)

    def _create_section(self, title: str, games: list):
        # 1. Root Container
        section_root = QFrame()
        section_layout = QVBoxLayout(section_root)

        # 2. Section Title
        section_name = QLabel(title)
        section_name.setObjectName("section_title")
        section_layout.addWidget(section_name)

        # 3. QListView
        list_view = HoverableListView()
        list_view.setObjectName("home_section_list_view")
        list_view.setViewMode(QListView.ViewMode.IconMode)
        list_view.setFlow(QListView.Flow.LeftToRight)
        list_view.setWrapping(False)
        list_view.setFixedHeight(200)
        list_view.setItemDelegate(GameCardDelegate())
        list_view.clicked.connect(self._handle_card_click)

        # 4. Model setup
        model = GameListModel(coordinator=self.view_model.coordinator.model)
        model.update_data(games)
        list_view.setModel(model)

        self.models[title] = model # Keep track to update later if needed

        section_layout.addWidget(list_view)
        self.ui.verticalLayout.addWidget(section_root)

    def _handle_card_click(self, index):
        # 'index' is the QModelIndex of the item clicked
        game_data = index.data(Qt.DisplayRole)
        logger.info(f"Card clicked: {game_data.title}")

        # Pass the data to the view model
        self.view_model._handle_card_click(game_data)

    def set_heros(self, heros: list):
        self._create_section("Featured", heros)

    def set_trending(self, games: list):
        self._create_section("Trending", games)

    def set_newest(self, games: list):
        self._create_section("Newest", games)

    def set_best_rated(self, games: list):
        self._create_section("Best Rated", games)
