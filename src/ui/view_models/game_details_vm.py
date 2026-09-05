from typing import TYPE_CHECKING, Callable

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QPixmap

from src.core.utils.log import get_logger

if TYPE_CHECKING:
    from src.core import AppCoordinator

logger = get_logger(__name__)


class GameDetailsViewModel(QObject):
    update_gallery = Signal(list)
    update_sys_req = Signal(dict)
    update_metadata = Signal(dict)
    reset = Signal()

    show_providers = Signal(dict)
    get_providers_failed = Signal(str)  # MSG or Status
    download_requested = Signal(
        str, str, str, str, object
    )  # save_path, url, id, name, banner
    download_cancelled = Signal(str)
    provider_state_changed = Signal(dict)

    set_poster = Signal(bytes)
    set_metadata = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.coordinator: AppCoordinator
        self.current_game_id: str | None = None

    def initialize(self, coordinator):
        self.coordinator = coordinator
        self.bind_signals()

    def bind_signals(self):
        self.coordinator.model.download_manager.providers_found.connect(
            self._handle_provider
        )

    @Slot(object)
    def load_card(self, card):
        self.reset.emit()
        if not card:
            return

        self.current_game_id = str(card.id)

        metadata_dict = {
            "title": card.title,
            "rating": card.rating,
            "rating_color": self._get_rating_color(card.rating),
            "released": card.released,
            "genres": card.genres,
            "metacritic": card.metacritic,
            "metacritic_color": self._get_metacritic_color(card.metacritic),
            "description": card.description,
        }
        self.set_metadata.emit(metadata_dict)

        self._get_gallery(card.id)

        banner: QPixmap = card.poster_pixmap
        if isinstance(banner, QPixmap) and not banner.isNull():
            logger.debug(f"Using cached banner for game: {card.id}")
            self.set_poster.emit(banner)
        else:
            logger.debug(f"Fetching remote poster for game: {card.id}")
            self._get_poster(card.id, card.background_image)

        # NOTE: SearchManager.get_system_req already caches by game_id,
        # so we always route through it rather than relying on a
        # per-card cache that is never actually populated.
        self._get_sys_req(card.id)

    def get_providers(self):
        game = self.coordinator.model.search_manager._games_list.get(self.current_game_id)
        slug = game.slug if game else None
        if slug:
            logger.debug(f"Fetching providers for game: {slug}")
            self.coordinator.model.download_manager.get_providers(slug)
        else:
            logger.warning(
                f"Could not find slug for game_id: {self.current_game_id} to fetch providers."
            )

    def request_download(
        self,
        save_path: str,
        provider_url: str,
        download_id: str,
        download_name: str = "NONAME",
        banner: QPixmap | None = None,
    ):
        self.download_requested.emit(
            save_path, provider_url, download_id, download_name, banner
        )

    def cancel_download(self, download_id: str):
        self.download_cancelled.emit(download_id)

    @Slot(object)
    def update_provider_state(self, download_model):
        logger.debug(f"Updating provider state for {download_model.id}")
        state = {
            "id": download_model.id,
            "progress": download_model.progress,
            "is_downloading": download_model.is_downloading,
            "has_finished": download_model.has_finished,
            "has_failed": download_model.has_failed,
        }
        self.provider_state_changed.emit(state)

    def _emit_if_current(self, game_id: str, signal: Signal, payload, label: str) -> None:
        """Guards against stale async responses overwriting the currently viewed game."""
        if self.current_game_id == game_id:
            logger.debug(f"Received {label} for [{game_id}], updating view.")
            signal.emit(payload)
        else:
            logger.info(
                f"Received {label} for [{game_id}], but current game is "
                f"[{self.current_game_id}]. Ignoring."
            )

    @Slot(dict, str)
    def _handle_system_req(self, reqs: dict, game_id: str):
        self._emit_if_current(game_id, self.update_sys_req, reqs, "system requirements")

    def _get_sys_req(self, game_id: str):
        logger.debug(f"Fetching system requirements for game_id: {game_id}")
        self.coordinator.task_runner.run_task(
            self.coordinator.model.search_manager.get_system_req,
            self._handle_system_req,
            game_id,
            return_value=game_id,
        )

    def _get_poster(self, game_id: str, url: str):
        logger.debug(f"Fetching poster for game_id: {game_id}")
        self.coordinator.task_runner.run_task(
            self.coordinator.model.asset_manager.get_thumbnail,
            self.handle_poster,
            game_id,
            url,
            return_value=game_id,
        )

    @Slot(bytes, str)
    def handle_poster(self, poster_data: bytes, game_id: str):
        self._emit_if_current(game_id, self.set_poster, poster_data, "poster")

    def _get_gallery(self, game_id: str):
        logger.debug(f"Fetching gallery for game_id: {game_id}")
        self.coordinator.task_runner.run_task(
            self.coordinator.model.asset_manager.get_screenshots,
            self.load_gallery,
            game_id,
            return_value=game_id,
        )

    @Slot(list, str)
    def load_gallery(self, screenshots: list[bytes], game_id: str):
        self._emit_if_current(game_id, self.update_gallery, screenshots, "screenshots")

    @Slot(dict)
    def _handle_provider(self, providers: dict):
        if providers:
            self.show_providers.emit(providers)
        else:
            self.get_providers_failed.emit("Retry")

    def _get_color(self, value: float | None = None, max_val: float = -1) -> str:
        if value is None or max_val <= 0:
            return "#aaaaaa"
        percentage = (value / max_val) * 100
        if percentage >= 75:
            return "#66cc33"  # Green
        elif percentage >= 50:
            return "#ffcc33"  # Yellow
        else:
            return "#ff3333"  # Red

    def _get_rating_color(self, rating: float) -> str:
        return self._get_color(rating, 5.0)

    def _get_metacritic_color(self, score: int) -> str:
        return self._get_color(score, 100.0)
