from PySide6.QtCore import QObject, Signal

class UiSignals(QObject):
    request_show_window = Signal(object)

class GameInfoWindowSignals(UiSignals):
    thumbnail_loaded = Signal(object)
    game_selected = Signal(object)
