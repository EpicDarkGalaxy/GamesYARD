from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap

# Singals for the worker threads
class WorkerSignals(QObject):
    fail = Signal()  # Signal to emit error messages
    finished = Signal()  # Signal to indicate the worker has finished
    cancelled = Signal()  # Signal to indicate the worker has been cancelled
    progress = Signal(float)  # Signal to emit progress updates

class ThumbnailWorkerSignals(WorkerSignals):
    thumbnail_fetch_finished = Signal(object, bytes)  # Signal to emit the list of fetched icons

class FetchWorkerSignals(WorkerSignals):
    fetch_finished = Signal(list)  # Signal to emit the list of fetched items
    fetch_fail = Signal() # Signal to indicate the worker has failed to fetch items

class DownloadWorkerSignals(WorkerSignals):
    download_finished = Signal(object)  # Signal to indicate the download has finished
    download_fail = Signal()  # Signal to indicate the download has failed

class LinkExtractorWorkerSignals(WorkerSignals):
    link_extracted = Signal(str, object)  # Signal to emit the extracted link and the URL
