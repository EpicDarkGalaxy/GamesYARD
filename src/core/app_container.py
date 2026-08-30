from typing_extensions import final

from ..ui.navigator import Navigator
from ..ui.view_models import *
from ..ui.views import *
from ..ui.views.pages import *
from .app_coordinator import AppCoordinator
from .app_core import AppCore


@final
class AppContainer:
    def __init__(self) -> None:
        self._model = AppCore()
        self._navigator = Navigator()

        # View Modles
        self._search_vm = SearchCatalogViewModel(self._model, self._navigator)
        self._game_details_vm = GameDetailsViewModel(self._model, self._navigator)
        self._main_vm: MainViewModel = MainViewModel(self._model, self._navigator)

        # Views
        self._main_view = MainView(self._main_vm, self._navigator)
        self._game_details_view = GameDetailsView(self._game_details_vm)
        self._search_catalog_view = SearchCatalogView(self._search_vm)

        # Init
        self._main_view.init_views(self._search_catalog_view, self._game_details_view)

        self._coordinator = AppCoordinator(
            self._search_vm,
            self._game_details_vm,
            self._navigator
        )

        self._search_vm.initialize(self._coordinator)
        self._game_details_vm.initialize(self._coordinator)
        self._main_vm.initialize(self._coordinator)
