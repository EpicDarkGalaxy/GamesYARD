
class SearchPagePersenter:
	def __init__(self, view, model) -> None:
		self.view = view
		self.model = view

	def add_to_grid(self, games):
	    self.view.update_grid(games)
