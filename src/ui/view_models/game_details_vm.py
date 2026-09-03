from typing import TYPE_CHECKING
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
    get_providers_failed = Signal(str) #  MSG or Status
    download_requested = Signal(str, str, str, str) # save_path, url, id, name
    download_cancelled = Signal(str)
    provider_state_changed = Signal(dict)

    set_title = Signal(str)
    set_rating = Signal(float, str)
    set_release = Signal(str)
    set_genres = Signal(list)
    set_metacritic = Signal(int, str)
    set_poster = Signal(bytes)

    def __init__(self) -> None:
        super().__init__()
        # will be initialized via initialize()
        self.coordinator: AppCoordinator

        # id of the currently viewed game
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
        if card:
            self.current_game_id = str(card.id)  # The card user is viewing
            title: str = card.title
            rating: float = card.rating
            released: str = card.released
            genres: list[str] = card.genres
            metacritic: int = card.metacritic
            banner: QPixmap = card.poster_pixmap

            self.set_title.emit(title)
            self.set_rating.emit(rating, self._get_rating_color(rating))
            self.set_release.emit(released)
            self.set_genres.emit(genres)
            self.set_metacritic.emit(metacritic, self._get_metacritic_color(metacritic))
            self._get_gallery(card.id)
            if isinstance(banner, QPixmap) and not banner.isNull():
                logger.debug(f"Using cached banner for game: {card.id}")
                self.set_poster.emit(banner)
            else:
                logger.debug(f"Fetching remote poster for game: {card.id}")
                self._get_poster(card.id, card.background_image)

            if card.system_requirements:
                logger.debug(f"Using cached system requirements for: {card.id}")
                self._handle_system_req(card.system_requirements, card.id)
            else:
                logger.debug(f"Fetching remote system requirements for: {card.id}")
                self._get_sys_req(card.id)

    @Slot()
    def get_providers(self):
        game_title = self.coordinator.model.search_manager._games_list.get(
            self.current_game_id
        ).title
        if game_title:
            logger.debug(f"Fetching providers for game: {game_title}")
            self.coordinator.model.download_manager.get_providers(game_title)
        else:
            logger.warning(
                f"Could not find title for game_id: {self.current_game_id} to fetch providers."
            )
                                                # download id is game id
    def request_download(self, save_path: str, provider_url: str, download_id: str, download_name: str="NONAME"):
        self.download_requested.emit(save_path, provider_url, download_id, download_name)

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

    @Slot(dict, str)
    def _handle_system_req(self, reqs: dict, game_id: str):
        if self.current_game_id == game_id:
            logger.debug(f"Received and populating system requirements for [{game_id}]")
            self.update_sys_req.emit(reqs)
        else:
            logger.info(
                f"Received requirements for [{game_id}], but current game is [{self.current_game_id}]. Ignoring."
            )

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
        if self.current_game_id == game_id:
            self.set_poster.emit(poster_data)
        else:
            logger.info(
                f"Received poster for [{game_id}], but current game is [{self.current_game_id}]. Ignoring."
            )

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
        if self.current_game_id == game_id:
            self.update_gallery.emit(screenshots)
        else:
            logger.info(
                f"Received screenshots for {game_id}, but current game is {self.current_game_id}. Ignoring."
            )

    @Slot(dict)
    def _handle_provider(self, providers: dict):
        if providers:
            self.show_providers.emit(providers)
        else:
            self.get_providers_failed.emit("Retry")

    def _get_color(self, value: float = -1, max_val: float = -1) -> str:
        if value and max_val:
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
