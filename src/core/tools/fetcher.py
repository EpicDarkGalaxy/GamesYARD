from ..models import GameCard
from .log import get_logger
from .utils import decodeBase64, parseHtml

logger = get_logger(__name__)

# For now the Target Url is hardcoded,
# but in the future it will be dynamic and can be changed by the user
MAIN_URL = "https://4fnet.org"

class GameFetcher:
    def __init__(self):
        self.gameList: list[GameCard] = []

    def get_game_list(self, query):
        self.gameList.clear() # Reset gameList to remove duplicates

        search_url = f"{MAIN_URL}/?s={query}"
        soup = parseHtml(search_url)
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

                logger.info(f"\n{"-" * 50}\nTITLE: {title} \nGAME PAGE: {main_page_link} \nPOSTER LINK: {poster_link}")

                logger.info(f"Adding game: {title}")
                self.gameList.append(GameCard(title, poster_link, main_page_link))

        if (self.gameList):
            return self.gameList
        else:
            logger.warning("No games found, returning empty list")
            return []

    def get_game_details(self, game_page_url):
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

    @staticmethod
    def fetch_download_links(game_url=None):
        if game_url is None:
            return []  # Return an empty list if no game URL is provided
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

        return download_links

# try:
#     selection = GameFetcher.gameList[int(input("SelectByNum: ")) - 1]
# except (ValueError):
#     print("Wrong Selection")
# except (IndexError):
#     print("Wrong Selection")
