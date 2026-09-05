from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QSizePolicy, QListView, QVBoxLayout, QWidget

from src.core.utils import get_logger
from src.ui.components.hoverable_list_view import HoverableListView
from src.ui.components import GameCard, LoadMoreButton
from src.ui.delegates.game_card_delegate import GameCardDelegate
from src.ui.generated import Ui_SearchGrid
from src.ui.layouts import FlowLayout
from src.ui.models.game_list_model import GameListModel

logger = get_logger(__name__)

class SearchCatalogView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.ui = Ui_SearchGrid()
        self.ui.setupUi(self)

        self.view_model = view_model

    def initialize(self):
        self._setup_list_view()
        self.bind_signals()

    def _setup_list_view(self):
        # Replace flow layout with ListView
        self.list_view = HoverableListView()
        self.list_view.setViewMode(QListView.IconMode)
        self.list_view.setWrapping(True)
        self.list_view.setResizeMode(QListView.Adjust)
        self.list_view.setSpacing(20)

        # Inject ListView into the existing UI layout
        layout = QVBoxLayout(self.ui.game_grid_container)
        layout.addWidget(self.list_view)

        self.model = GameListModel(coordinator=self.view_model.coordinator)
        self.list_view.setModel(self.model)
        self.list_view.setItemDelegate(GameCardDelegate())
        self.list_view.clicked.connect(self._handle_card_click)

    def bind_signals(self):
        self.view_model.update_grid.connect(self.update_grid)

    @Slot(list)
    def update_grid(self, games, clear_grid: bool = True):
        logger.info("SearchGridPage: updating search Grid")
        self.model.update_data(games)

    def _handle_card_click(self, index):
        # 'index' is the QModelIndex of the item clicked
        game_data = index.data(Qt.DisplayRole)
        logger.info(f"Card clicked: {game_data.title}")

        # Pass the data to the view model
        self.view_model._handle_card_click(game_data)

    def hideEvent(self, event):
        self.view_model._handle_search_catalog_hide()
