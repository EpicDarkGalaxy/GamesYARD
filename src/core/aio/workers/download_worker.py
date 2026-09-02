import os

from curl_cffi import requests as r

from ...utils.log import get_logger
from ..base_worker import BaseWorker
from ..worker_signals import DownloadWorkerSignals

logger = get_logger(__name__)

class DownloadWorker(BaseWorker):
    def __init__(self, url: str, save_path: str, download_id: str=""):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.download_id = download_id
        self.is_cancelled = False
        self.signals = DownloadWorkerSignals()

    def cancle(self):
        self.is_cancelled = True

    def run(self):
        logger.debug(f"Download Started for ID: [{self.download_id}]")
        try:
            response = r.get(self.url, stream=True, impersonate="chrome124")
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            with open(self.save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if (self.is_cancelled):
                        response.close()
                        f.close()
                        if (os.path.exists(self.save_path)):
                            os.remove(self.save_path)
                        logger.info(f"Download Cancelled: {self.download_id}")
                        self.signals.cancelled.emit()
                        return
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size:
                        percent = int(downloaded_size / total_size * 100)
                        self.signals.download_progress.emit(self.download_id ,percent)
            response.close()
            self.signals.download_finished.emit(self.download_id)
            self.signals.finished.emit()

        except Exception as e:
            self.signals.download_fail.emit(self.download_id)
            logger.error(f"failed to download {self.url} {e}")
