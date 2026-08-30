from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QSizePolicy, QWidget

from src.core.utils import get_logger
from src.ui.layouts import FlowLayout
from src.ui.generated import Ui_SearchGrid
from src.ui.components import GameCard, LoadMoreButton

logger = get_logger(__name__)

class SearchCatalogView(QWidget):
	card_created = Signal(object)
	card_clicked = Signal(object)

	def __init__(self, view_model):
		super().__init__()
		self.ui = Ui_SearchGrid()
		self.ui.setupUi(self)

		self.view_model = view_model

		self.ui.scrollArea.setWidgetResizable(True)
		self.ui.game_grid_container.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Expanding
		)
		self.flow_layout = FlowLayout(self.ui.game_grid_container, margin=20, spacing=20)

		self.bind_signals()


	def bind_signals(self):
		self.view_model.update_grid.connect(self.update_grid)

	@Slot(list)
	def update_grid(self, games, clear_grid: bool=True):
		logger.info("SearchGridPage: updating search Grid")

		# Clear existing widgets, ensuring we remove all LoadMoreButtons and GameCards
		while self.flow_layout.count():
			item = self.flow_layout.takeAt(0)
			if item and item.widget():
				item.widget().deleteLater()

		for game in games:
			game_card = GameCard(game)

			self.view_model.save_card(game_card)

			game_card.clicked.connect(lambda card: self.view_model._handle_card_click(card))
			game_card.request_thumbnail.connect(lambda card_id, url: self.view_model.get_thumb(card_id, url))

			self.flow_layout.addWidget(game_card)
			self.card_created.emit(game_card)

		# Add "Load More" button at the end
		load_more_btn = LoadMoreButton()
		self.flow_layout.addWidget(load_more_btn)
