class GamePagePresenter:
	def __init__(self, view, model) -> None:
		self.view = view
		self.model = model

	def load_card(self, card):
	    self.view.display(card)
