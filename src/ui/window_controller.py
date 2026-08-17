from .windows import GameInfoWindow, MainWindow

class WindowController:
    def __init__(self, manager):
        self.manager = manager
        self._main_window = None
        self.game_info_window = None
        self.manager.signals.show_game_info_window.connect(self.show_GameInfoWindow)

    def show_MainWindow(self):
        self._main_window = MainWindow(self.manager)
        self._show_Window(self._main_window)

    def show_GameInfoWindow(self):
        self._game_info_window = GameInfoWindow(self.manager)
        self._show_Window(self._game_info_window)

    @staticmethod
    def _show_Window(window):
        window.show()
