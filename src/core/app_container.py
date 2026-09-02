from typing_extensions import final

from src.core.app_coordinator import AppCoordinator
from src.core.app_core import AppCore
from src.ui.navigator import Navigator
from src.ui.view_models import *
from src.ui.views import *
from src.ui.views.pages import *


@final
class AppContainer:
    def __init__(self) -> None:
        self._APP_CORE = AppCore()
        self._NAVIGATOR = Navigator()

        # View Models
        self._view_models = {
            "search": SearchCatalogViewModel(),
            "details": GameDetailsViewModel(),
            "main": MainViewModel(),
            "home": HomeCatalogViewModel(),
        }

        # Views
        self._main_view = MainView(self._view_models["main"], self._NAVIGATOR)
        self._views = [
            SearchCatalogView(self._view_models["search"]),
            GameDetailsView(self._view_models["details"]),
            HomeCatalogView(self._view_models["home"]),
        ]

        self._coordinator = AppCoordinator(
            self._view_models["main"],
            self._view_models["search"],
            self._view_models["details"],
            self._view_models["home"],
            self._NAVIGATOR,
            self._APP_CORE
        )

        for vm in self._view_models.values():
            vm.initialize(self._coordinator)

        self._main_view.initialize(*self._views)

        for view in self._views:
            view.initialize()
