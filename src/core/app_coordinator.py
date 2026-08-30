class AppCoordinator:
    def __init__(self, search_vm, game_details_vm, nav) -> None:
        self.search_vm = search_vm
        self.game_details_vm = game_details_vm
        self.nav = nav

    def forward_card(self, card):
        self.game_details_vm.load_card(card)

    def forward_search_result(self, result):
        self.search_vm.add_to_grid(result)
