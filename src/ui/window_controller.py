from .windows import GameWindow, MainWindow
from .presenters import GamePresenter


class WindowController:
    def __init__(self, manager):
        self.manager = manager
        self.window_list = []
        self._main_window = None
        self.game_info_window = None
        self.manager.signals.show_game_info_window.connect(self.show_GameInfoWindow)
        self.manager.signals.shutting_down.connect(self._Close_AllWindows)


    def show_MainWindow(self):
        self._main_window = MainWindow()
        self._show_Window(self._main_window)
        self.window_list.append(self._main_window)

    def show_GameInfoWindow(self):
        self._game_info_window = GameWindow()
        self.game_presenter = GamePresenter(self._game_info_window, self.manager)
        self._show_Window(self._game_info_window)
        self.window_list.append(self._game_info_window)

    def _Close_AllWindows(self):
        for window in self.window_list:
            window.close()
        self.window_list.clear()

    @staticmethod
    def _show_Window(window):
        window.show()
