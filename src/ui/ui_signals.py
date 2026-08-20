from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QPushButton, QWidget


class UiSignals(QObject):
    update_btn = Signal(QPushButton)

class MainPresenterSignals(UiSignals):
    show_game_info_window = Signal()
    on_card_clicked = Signal(object)

class GameWindowSignals(UiSignals):
    thumbnail_loaded = Signal(object)
    fetch_btn_clicked = Signal()


class MainWindowSignals(UiSignals):
    fetch_btn_clicked = Signal(str)
    search_text_changed = Signal(str)

class ManagerSignals(UiSignals):
    cards_ready = Signal(list, bool)
    update_fetch_btn = Signal(str, bool)
    thumb_fetched = Signal(str, bytes)
    card_clicked = Signal(object)
    load_more = Signal()
    show_game_info_window = Signal()
    shutting_down = Signal()
