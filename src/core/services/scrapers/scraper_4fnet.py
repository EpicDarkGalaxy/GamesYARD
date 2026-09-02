import requests
from bs4 import BeautifulSoup

from src.core.utils import decodeBase64, get_logger

logger = get_logger(__name__)

class FourFNetScraper:
    def __init__(self):
        self.base_url = "https://4fnet.org"
        self.session = requests.Session()

    def find_game_page(self, game_title: str) -> str | None:
        """
        Takes the title from metadata, searches 4fnet,
        and returns the URL of the first (best) result.
        """
        search_url = f"{self.base_url}/?s={game_title}"
        try:
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get the first search result link
            first_article = soup.select_one("#post-items li a")
            if first_article:
                href = first_article.get("href")
                return str(href) if href else None

            logger.info(f"No search results found for: {game_title}")
            return None
        except requests.RequestException as e:
            logger.error(f"Search request failed for '{game_title}' at {search_url}: {e}")
            return None

    def fetch_download_links(self, game_url: str) -> dict[str, str]:
        """Extracts all decoded download links from a specific game page."""
        try:
            response = self.session.get(game_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            decoded_links: dict[str, str] = {}
            # Focus only on the 'goto' links which contain the download hosters
            links = soup.select("a[href*='/goto/']")
            if not links:
                logger.warning(f"No download links found on page: {game_url}")
                return {}

            for a in links:
                href = a.get("href")
                if isinstance(href, str):
                    # Handle the case where the base64 is in the path
                    path = href.split("/goto/")[-1]
                    decoded_url = decodeBase64(path)
                    # Extract the domain as the site name
                    site_name = decoded_url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]
                    decoded_links[site_name] = decoded_url

            logger.info(f"Successfully extracted {len(decoded_links)} download links from {game_url}")
            return decoded_links
        except requests.RequestException as e:
            logger.error(f"Request failed while fetching download links from {game_url}: {e}")
            return {}
        except Exception as e:
            logger.error(f"An unexpected error occurred while processing {game_url}: {e}")
            return {}
