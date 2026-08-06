from PySide6.QtCore import (Signal, QObject)

# Singals for the worker threads
class WorkerSignals(QObject):
    fail_signal = Signal(str)  # Signal to emit error messages
    finished_signal = Signal()  # Signal to indicate the worker has finished
    

class IconWorkerSignals(WorkerSignals):
    icon_fetched = Signal(int, bytes)  # Signal to emit the list of fetched icons

class FetchWorkerSignals(WorkerSignals):
    fetch_finished = Signal(list)  # Signal to emit the list of fetched items
    fetch_fail = Signal() # Signal to indicate the worker has failed to fetch items