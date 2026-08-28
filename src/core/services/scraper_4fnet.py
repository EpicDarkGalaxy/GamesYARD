from typing import List
from .base_fetcher import BaseGameFetcher
from ..models.game import GameData
from ..utils.utils import parseHtml, decodeBase64, get_logger

logger = get_logger(__name__)

class Scraper4fnetFetcher(BaseGameFetcher):
    def __init__(self):
        self.TARGET_URL = "https://4fnet.org"
        self.gameList = []

    def search_games(self, query: str, page: int = 1) -> list[GameData]:
        """
        Fetches the game list from the target URL based on the given query.

        Args:
            query (str): The search query to filter games.
            requery (bool): Whether to requery the first page or load the next page.

        Returns:
            list[GameData]: The list of fetched game data or an empty list if no games are found.
        """

        self.gameList.clear()

        search_url = f"{self.TARGET_URL}/page/{self.page}/?s={query}"
        soup = parseHtml(search_url)
        pagination = soup.select_one(".pagination")
        self.has_next_page = pagination is not None and "next" in pagination.text.lower()
        articles = soup.select("#post-items li")

        if (len(articles) > 0):
            logger.info(f"Found {len(articles)} articles")

            # Loop through your article selectors
            for element in articles:
                title_el = element.select_one("h2")

                title = title_el.text.strip() if title_el else ""

                anchor = element.select_one("a")
                main_page_link = anchor.get("href", "") if anchor else ""

                img = element.select_one("img")
                poster_link = img.get("src", "") if img else ""

                p = element.select_one("p")
                description = p.text.strip() if p else ""

                # logger.info(
                #     f"\n{'-' * 50}\nTITLE: {title} \nGAME PAGE: {main_page_link} \nPOSTER LINK: {poster_link}"
                # )

                logger.info(f"Adding game: {title}")
                self.gameList.append(GameData(
                    id=1,
                    title=title,
                    poster_url=poster_link,
                    game_url=main_page_link,
                    description=description,
                    rating=0.0,
                    metacritic=0
                ))

        if (self.gameList):
            return self.gameList
        else:
            logger.warning("No games found, returning empty list")
            return []

    def get_game_details(self, game_page_url: str) -> dict:
        """
        Fetches the game details from the game page URL where game details are located.

        Args:
            game_page_url (str): The URL of the game page.

        Returns:
            dict: The parsed game details or an empty dictionary if no details are found.
        """
        soup1 = parseHtml(game_page_url)
        tr = soup1.select("tr")
        tr.pop(0) if tr else None # We don't need the first row

        system_requirement = {}
        for element in tr:
            th = element.select_one("th")
            td = element.select_one("td")

            if th and td:
                key = th.text.strip()
                if (key.lower() == "languages:"): # Languages is the last row
                    break
                value = td.text.strip()
                system_requirement[key] = value

        # Print system requirements in a readable format
        # logger.info("\n-------System Requirements-------\n")
        # for key, value in system_requirement.items():
        #     logger.info(f"[{key}] {value}")

        return system_requirement

    def fetch_download_links(self, game_url: str) -> list[str]:
        """
        Fetches the providers links from the game page URL where download links are located.

        Args:
            game_url (str): The URL of the game page.

        Returns:
            list: The list of fetched provider links or an empty list if no links are found.
        """

        if not game_url:
            logger.warning("GAME URL is Empty")
            return []  # Return an empty list if no game URL is provided

        logger.info(f"Fetching hosts from URL: {game_url}")
        soup2 = parseHtml(game_url)
        download_links = []
        for element in soup2.select("a"):
            href = element.get("href")
            if href and "/goto/" in href:
                decoded_link = decodeBase64(href)
                download_links.append(decoded_link)

        # Print download links
        logger.info("Donwload Links (unprocessed)")
        for link in download_links:
            logger.info(link)

        if (download_links):
            return download_links
        return []
