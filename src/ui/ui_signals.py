from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QPushButton, QWidget


class UiSignals(QObject):
    update_btn = Signal(QPushButton)

class GameInfoWindowSignals(UiSignals):
    thumbnail_loaded = Signal(object)

class MainWindowSignals(UiSignals):
    pass

class ManagerSignals(UiSignals):
    cards_ready = Signal(list)
    update_fetch_btn = Signal(str, bool)
    card_clicked = Signal(object)
    show_game_info_window = Signal()
