from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QPushButton, QWidget


class UiSignals(QObject):
    update_btn = Signal(QPushButton)
    close = Signal(object)

class MainPresenterSignals(UiSignals):
    show_game_info_window = Signal()
    on_card_clicked = Signal(object)

class GameWindowSignals(UiSignals):
    thumbnail_loaded = Signal(object)
    fetch_btn_clicked = Signal()
    closing_window = Signal()

class MainWindowSignals(UiSignals):
    fetch_btn_clicked = Signal(str)
    search_text_changed = Signal(str)
