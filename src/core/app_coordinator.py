from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.core.aio.task_runner import TaskRunner
    from src.core.managers import *

class AppCoordinator:
    def __init__(
        self,
        main_vm: Any,
        search_vm: Any,
        game_details_vm: Any,
        home_vm: Any,
        download_vm: Any,
        nav: Any,
        app_core: Any
    ) -> None:
        self.main_vm: Any = main_vm
        self.search_vm: Any = search_vm
        self.game_details_vm: Any = game_details_vm
        self.home_vm: Any = home_vm
        self.download_vm: Any = download_vm
        self._nav: Any = nav
        self.model: Any = app_core

        self.task_runner: TaskRunner = self.model.task_runner
        self.asset_manager: AssetManager = self.model.asset_manager
        self.download_manager: DownloadManager = self.model.download_manager
        self.search_manager: SearchManager = self.model.search_manager

        self.bind_view_models()

    def bind_view_models(self) -> None:
        # Connects to game_details_vm
        self.search_vm.card_clicked.connect(self.game_details_vm.load_card)
        self.home_vm.card_clicked.connect(self.game_details_vm.load_card)
        self.download_vm.update_view.connect(self.game_details_vm.update_provider_state)

        # Connects to search_vm
        self.main_vm.search_finished.connect(self.search_vm.add_to_grid)

        # Connects to download_vm
        self.game_details_vm.download_requested.connect(self.download_vm.download)

    def navigate(self, key: str) -> None:
        self._nav.go_to(key)

    def navigate_back(self) -> None:
        self._nav.go_to_last_nav()
