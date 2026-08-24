import logging

from .windows import GameWindow, MainWindow
from .presenters import GamePresenter, MainPresenter

logger = logging.getLogger(__name__)


class WindowController:
    def __init__(self, manager):
        self.manager = manager
        self.window_list = []
        self.presenter_list = []


        self.manager.signals.show_game_info_window.connect(self.show_GameInfoWindow)
        self.manager.signals.shutting_down.connect(self.close_AllWindows)


    def show_MainWindow(self):
        logger.info("Showing Main Window")
        main_window = MainWindow()
        main_presenter = MainPresenter(main_window, self.manager, self)
        self._show_Window(main_window)
        self.presenter_list.append(main_presenter)
        self.window_list.append(main_window)

    def show_GameInfoWindow(self):
        logger.info("Showing Game Info Window")
        game_window = GameWindow()
        game_presenter = GamePresenter(game_window, self.manager)
        self._show_Window(game_window)
        self.presenter_list.append(game_presenter)
        self.window_list.append(game_window)

    def close_AllWindows(self):
        logger.info("Closing all windows")
        for window in self.window_list:
            window.close()
        self.window_list.clear()

    @staticmethod
    def _show_Window(window):
        window.show()
