import base64
from typing import override

import requests
from bs4 import BeautifulSoup

from src.core.services.scrapers.base_scraper import BaseScraper
from src.core.utils.log import get_logger

logger = get_logger(__name__)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


class GameBountyScraper(BaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://gamebounty.world"
        self.session = requests.Session()
        self.session.headers.update(_HEADERS)

    @staticmethod
    def _decode_dl_url(encoded: str) -> str:
        # The base64 embedded in these links is sometimes missing trailing
        # '=' padding, since it's URL-embedded. Restore it before decoding.
        padded = encoded + "=" * (-len(encoded) % 4)
        return base64.b64decode(padded).decode("utf-8")

    def find_game_url(self, game_title: str) -> str | None:
        search_url = f"{self.base_url}/api/v1/search"
        params = {"q": game_title, "page": 1, "size": 5, "sort": "relevance"}

        try:
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = data.get("data", {}).get("results", [])
            if not results:
                logger.info(f"No GameBounty results found for: {game_title}")
                return None

            best_match = results[0]  # API already ranks by relevance
            slug = best_match.get("slug")
            if not slug:
                return None

            game_url = f"{self.base_url}/{slug}-free-pc-download"
            logger.info(
                f"GameBounty match for '{game_title}': "
                f"'{best_match.get('title')}' -> {game_url}"
            )
            return game_url

        except requests.RequestException as e:
            logger.error(f"GameBounty search request failed for '{game_title}': {e}")
            return None
        except (ValueError, KeyError) as e:
            logger.error(f"Failed to parse GameBounty search response for '{game_title}': {e}")
            return None

    @override
    def scrape_download_urls(self, game_url: str) -> dict[str, dict[str, str]]:
        """Extracts all decoded mirror links from a GameBounty game page."""
        try:
            response = self.session.get(game_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            decoded_links: dict[str, str] = {}
            links = soup.select("a[href*='/api/dl/']")
            if not links:
                logger.warning(f"No download links found on GameBounty page: {game_url}")
                return {}

            for a in links:
                href = a.get("href")
                if not isinstance(href, str):
                    continue

                encoded = href.rstrip("/").split("/")[-1]
                try:
                    decoded_url = self._decode_dl_url(encoded)
                except Exception as e:
                    logger.warning(f"Failed to decode GameBounty link '{href}': {e}")
                    continue

                site_name = (
                    decoded_url.split("//")[-1]
                    .split("/")[0]
                    .replace("www.", "")
                    .split(".")[0]
                )
                decoded_links[site_name] = decoded_url

            logger.info(
                f"Extracted {len(decoded_links)} download links from GameBounty page: {game_url}"
            )
            return {"GameBounty": decoded_links}

        except requests.RequestException as e:
            logger.error(f"Request failed while fetching GameBounty page {game_url}: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error scraping GameBounty page {game_url}: {e}")
            return {}
