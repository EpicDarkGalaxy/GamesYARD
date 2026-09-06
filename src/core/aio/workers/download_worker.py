import os
import time

from curl_cffi import requests

from ...utils.log import get_logger
from ..base_worker import BaseWorker
from ..worker_signals import DownloadWorkerSignals

logger = get_logger(__name__)

class DownloadWorker(BaseWorker):
    def __init__(
        self,
        url: str,
        save_path: str,
        download_id: str = "",
        download_headers: dict | None = None
    ):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.download_id = download_id
        self.can_emit_state = False
        self.resume_supported = False
        self.is_cancelled = False
        self.is_paused = False
        # Fix #1: Avoid mutable default argument
        self.headers = dict(download_headers) if download_headers else {}
        self.signals = DownloadWorkerSignals()
        self.session = requests.Session()

    def cancel(self):
        self.is_cancelled = True

    def pause(self):
        self.is_paused = True

    def _emit_state(self, downloaded_size: int, total_size: int, speed: float, is_downloading: bool):
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
            "eta": self._calculate_eta(downloaded_size, total_size, speed)
        })

    def _calculate_eta(self, downloaded_size: int, total_size: int, speed: float) -> float:
        if not speed or not total_size or downloaded_size >= total_size:
            return 0.0
        return (total_size - downloaded_size) / speed

    def _get_remote_size(self, headers: dict) -> int:
        """Check remote file size via HEAD request."""
        try:
            head_resp = self.session.head(self.url, impersonate="chrome124", headers=headers, timeout=10)
            return int(head_resp.headers.get('content-length', 0))
        except Exception as e:
            logger.warning(f"HEAD request failed for {self.url}: {e}. Proceeding with GET.")
            return 0

    def _check_already_downloaded(self, remote_size: int) -> bool:
        """Check if file is already fully downloaded."""
        if remote_size > 0 and os.path.exists(self.save_path):
            local_size = os.path.getsize(self.save_path)
            if local_size >= remote_size:
                logger.info(f"File {self.download_id} is already fully downloaded ({local_size}/{remote_size} bytes). Skipping.")
                self._emit_state(local_size, remote_size, 0.0, is_downloading=False)
                self.signals.download_finished.emit(True, self.download_id)
                self.signals.finished.emit()
                return True
        return False

    def _prepare_download_headers(self) -> tuple[dict, int]:
        """Prepare headers and starting position for resuming."""
        headers = dict(self.headers)
        downloaded_size = 0

        if os.path.exists(self.save_path):
            downloaded_size = os.path.getsize(self.save_path)

        if downloaded_size > 0:
            headers["Range"] = f"bytes={downloaded_size}-"
            logger.info(f"Resuming download {self.download_id} from byte {downloaded_size}")

        return headers, downloaded_size

    def _handle_response_status(self, response, downloaded_size: int) -> tuple[int, str]:
        """Determine file writing mode based on server range support."""
        accept_ranges = response.headers.get("accept-ranges", "").lower()

        if response.status_code == 206 or "bytes" in accept_ranges:
            logger.info(f"Download {self.download_id} supports resuming")
            self.resume_supported = True
            file_mode = 'ab'
        else:
            if downloaded_size > 0:
                logger.warning(f"Server ignored Range header for {self.download_id}. Restarting download from scratch.")
            downloaded_size = 0
            file_mode = 'wb'

        return downloaded_size, file_mode

    def _handle_cancellation(self, response) -> bool:
        if self.is_cancelled:
            response.close()
            logger.info(f"Download Cancelled: {self.download_id}")
            self.signals.cancelled.emit(self.download_id)
            self.signals.finished.emit()
            return True
        return False

    def _handle_pause(self, response, downloaded_size: int, total_size: int) -> bool:
        if self.is_paused:
            response.close()
            logger.info(f"Download Paused: {self.download_id} at {downloaded_size} bytes")
            self._emit_state(downloaded_size, total_size, 0.0, is_downloading=False)
            self.signals.paused.emit(self.download_id)
            self.signals.finished.emit()
            return True
        return False

    def run(self):
        logger.debug(f"Download Started for ID: [{self.download_id}]")
        try:
            remote_size = self._get_remote_size(self.headers)

            if self._check_already_downloaded(remote_size):
                return

            req_headers, initial_downloaded_size = self._prepare_download_headers()
            response = requests.get(
                self.url,
                stream=True,
                headers=req_headers,
                timeout=10,
                allow_redirects=True
            )

            downloaded_size, file_mode = self._handle_response_status(response, initial_downloaded_size)

            self.can_emit_state = True
            response.raise_for_status()

            content_length = int(response.headers.get('content-length', 0))

            if response.status_code == 206:
                total_size = downloaded_size + content_length
            else:
                total_size = content_length

            total_size = max(total_size, remote_size)

            self._emit_state(downloaded_size, total_size, 0.0, is_downloading=True)

            start_time = time.time()
            bytes_this_session = 0

            with open(self.save_path, file_mode) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if self._handle_cancellation(response):
                        return

                    if self._handle_pause(response, downloaded_size, total_size):
                        return

                    f.write(chunk)
                    chunk_len = len(chunk)
                    downloaded_size += chunk_len
                    bytes_this_session += chunk_len

                    current_time = time.time()
                    elapsed_time = current_time - start_time

                    if elapsed_time >= 1.0:
                        speed_bytes_per_sec = bytes_this_session / elapsed_time
                        if self.can_emit_state:
                            self._emit_state(downloaded_size, total_size, speed_bytes_per_sec, is_downloading=True)
                        start_time = current_time
                        bytes_this_session = 0

            response.close()

            # Final completion state update
            final_size = total_size if total_size else downloaded_size
            self._emit_state(final_size, final_size, 0.0, is_downloading=False)

            self.signals.download_finished.emit(True, self.download_id)
            self.signals.finished.emit()

        except Exception as e:
            self.signals.download_finished.emit(False, self.download_id)
            self.signals.finished.emit()
            logger.error(f"failed to download {self.url}: {e}")
