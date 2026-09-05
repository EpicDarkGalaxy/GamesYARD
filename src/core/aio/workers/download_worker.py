import os
import time

from curl_cffi import requests as r

from ...utils.log import get_logger
from ..base_worker import BaseWorker
from ..worker_signals import DownloadWorkerSignals

logger = get_logger(__name__)

class DownloadWorker(BaseWorker):
    def __init__(self, url: str, save_path: str, download_id: str = ""):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.download_id = download_id
        self.can_emit_state = False
        self.resume_supported = False
        self.is_cancelled = False
        self.is_paused = False
        self.signals = DownloadWorkerSignals()

    def cancel(self):
        self.is_cancelled = True

    def pause(self):
        self.is_paused = True

    def _emit_state(self, downloaded_size, total_size, speed, is_downloading):
        percent = int(downloaded_size / total_size * 100) if total_size else 0
        self.signals.download_progress.emit({
            "download_id": self.download_id,
            "percent": percent,
            "downloaded_size": downloaded_size,
            "total_size": total_size,
            "paused": self.is_paused,
            "is_downloading": is_downloading,
            "resume_supported": self.resume_supported,
            "speed": speed,
        })

    def run(self):
        logger.debug(f"Download Started for ID: [{self.download_id}]")
        try:
            downloaded_size = 0
            if os.path.exists(self.save_path):
                downloaded_size = os.path.getsize(self.save_path)

            headers = {}
            if downloaded_size > 0:
                headers["Range"] = f"bytes={downloaded_size}-"
                logger.info(f"Resuming download {self.download_id} from byte {downloaded_size}")

            response = r.get(self.url, stream=True, impersonate="chrome124", headers=headers, timeout=10)
            if response.status_code == 206:
                logger.info(f"Download {self.download_id} supports resuming")
                self.resume_supported = True
                self.can_emit_state = True

            response.raise_for_status()

            content_length = int(response.headers.get('content-length', 0))
            total_size = downloaded_size + content_length if downloaded_size else content_length

            file_mode = 'ab' if downloaded_size > 0 else 'wb'

            start_time = time.time()
            bytes_this_session = 0

            with open(self.save_path, file_mode) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if self.is_cancelled:
                        response.close()
                        if os.path.exists(self.save_path):
                            os.remove(self.save_path)
                        logger.info(f"Download Cancelled: {self.download_id}")
                        self.signals.cancelled.emit()
                        return

                    # By this point in the code, headers are ALREADY parsed,
                    # so resume_supported/total_size are guaranteed known.
                    if self.is_paused:
                        response.close()
                        logger.info(f"Download Paused: {self.download_id} at {downloaded_size} bytes")
                        # Emit the FULL, up-to-date state instead of just an ID
                        self._emit_state(downloaded_size, total_size, 0.0, is_downloading=False)
                        self.signals.download_paused.emit(self.download_id)
                        return

                    f.write(chunk)
                    downloaded_size += len(chunk)
                    bytes_this_session += len(chunk)

                    elapsed_time = time.time() - start_time
                    speed_bytes_per_sec = bytes_this_session / elapsed_time if elapsed_time > 0 else 0.0

                    if total_size and self.can_emit_state:
                        self._emit_state(downloaded_size, total_size, speed_bytes_per_sec, is_downloading=True)

            response.close()
            self.signals.download_finished.emit(True, self.download_id)
            self.signals.finished.emit()

        except Exception as e:
            self.signals.download_finished.emit(False, self.download_id)
            logger.error(f"failed to download {self.url} {e}")
