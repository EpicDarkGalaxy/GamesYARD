from .log import get_logger
from .models import GameCardData, GameDetails
from .utils import decodeBase64, parseHtml

logger = get_logger(__name__)

# For now the Target Url is hardcoded,
# but in the future it will be dynamic and can be changed by the user
MAIN_URL = "https://4fnet.org"

class GameFetcher:
    gameList = []
    counter = 1 # index

    def get_game_list(self, query):
        self.gameList = [] # Reset gameList to remove duplicates
        self.counter = 0 # Reset counter to prevent index out of range

        search_url = f"{MAIN_URL}/?s={query}"
        soup = parseHtml(search_url)

        if (len(soup.contents) > 0):
            # Loop through your article selectors
            articles = soup.select("ul li")

            logger.info(f"Found {len(articles)} articles")

            for element in articles:
                title_el = element.select_one("h2")

                title = title_el.text.strip() if title_el else ""

                anchor = element.select_one("a")
                href = anchor.get("href", "") if anchor else ""

                img = element.select_one("img")
                poster = img.get("src", "") if img else ""

                if title:
                    print(f"Selection Number: {self.counter}")
                    print(f"Title:  {title}")
                    print(f"Href:   {href}")
                    print(f"Poster: {poster}")
                    print("-" * 40)
                    self.gameList.append(GameCardData(title, href, poster, None, downloads_links=[]))  # posterPixmap will be set later
                self.counter = self.counter + 1

        return self.gameList

    def get_game_details(self, game_data):
        if not game_data.href:
            return GameDetails(title="", href="", posterLink="", posterPixmap=None, downloads_links=[], system_requirements={})

        soup1 = parseHtml(game_data.href)
        tr = soup1.select("tr")
        tr.pop(0) if tr else None

        system_requirement = {}
        for element in tr:
            th = element.select_one("th")
            td = element.select_one("td")

            if th and td:
                key = th.text.strip()
                if (key.lower() == "languages:"):
                    break
                value = td.text.strip()
                system_requirement[key] = value

        # Print system requirements in a readable format
        logger.info("\n-------System Requirements-------\n")
        for key, value in system_requirement.items():
            logger.info(f"[{key}] {value}")

        game_details = GameDetails(
            title=game_data.title if game_data else "",
            href=game_data.href if game_data else "",
            posterLink=game_data.posterLink if game_data else "",
            posterPixmap=game_data.posterPixmap if game_data else None,
            system_requirements=system_requirement,
            downloads_links=[]
        )
        return game_details

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
        logger.info("Donwload Links (not processed)")
        for link in download_links:
            logger.info(link)

        return download_links

# try:
#     selection = GameFetcher.gameList[int(input("SelectByNum: ")) - 1]
# except (ValueError):
#     print("Wrong Selection")
# except (IndexError):
#     print("Wrong Selection")
