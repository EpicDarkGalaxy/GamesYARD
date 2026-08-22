from PySide6.QtCore import QObject, Signal


class Signals(QObject):
    cards_ready = Signal(list, bool)
    update_fetch_btn = Signal(str, bool)
    thumb_fetched = Signal(str, bytes)
    card_clicked = Signal(object)
    load_more = Signal()
    show_game_info_window = Signal()
    opened_card_changed = Signal(object)
    shutting_down = Signal()
    download_progress = Signal(int)
    download_finished = Signal(str)
