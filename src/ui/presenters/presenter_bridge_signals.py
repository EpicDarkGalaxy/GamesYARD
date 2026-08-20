from PySide6.QtCore import QObject, Signal

class PresenterBridgeSignals(QObject):
    card_clicked_to_show = Signal(object)

PRESENTER_BRIDGE_SIGNALS = PresenterBridgeSignals()
