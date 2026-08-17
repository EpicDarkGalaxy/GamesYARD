from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QPushButton, QWidget


class UiSignals(QObject):
    update_btn = Signal(QPushButton)


class GameInfoWindowSignals(UiSignals):
    thumbnail_loaded = Signal(object)
    game_selected = Signal(object)


class MainWindowSignals(UiSignals):
    request_show_window = Signal(QWidget)
    add_to_grid = Signal(QWidget)
    update_fetch_btn = Signal(str, bool)
