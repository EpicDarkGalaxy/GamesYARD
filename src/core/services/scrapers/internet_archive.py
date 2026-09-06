from curl_cffi import requests
from typing import override
from src.core.services.scrapers.base_scraper import BaseScraper
from src.core.utils import get_logger

logger = get_logger(__name__)

class InternetArchiveScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self._search_api = "https://archive.org/advancedsearch.php"
        self._metadata_api = "https://archive.org/metadata"

        self.blocked_keywords = ["DOC", "DOCS", "ART", "ARTS", "ICON", "ICONS", "GUIDE", "GUIDES"]
        self.keywords = ["GOG", "DLC"]

    @override
    def find_game_url(self, game_title: str) -> str | None:
        """
        Searches Internet Archive for items matching the game title,
        fetches multiple candidates, scores/filters them to avoid soundtracks/manuals,
        and returns the identifier of the best matching item.
        """
        clean_title = game_title.strip()
        base_query = f'title:("{clean_title}") AND mediatype:(software)'

        # Try keyword query first if keywords exist
        keyword_query = None
        if self.keywords:
            kw_str = " OR ".join([f'title:("{kw}")' for kw in self.keywords])
            keyword_query = f'title:("{clean_title}") AND ({kw_str}) AND mediatype:(software)'

        params = {
            "fl[]": "identifier,title,downloads,collection",
            "sort[]": "downloads desc", # Prioritize popular/downloaded items
            "rows": 10,                 # Fetch top candidates for scoring
            "output": "json",
        }

        try:
            docs = []
            # 1. Try keyword-boosted query
            if keyword_query:
                params["q"] = keyword_query
                response = requests.get(self._search_api, params=params, impersonate="chrome124", timeout=10)
                docs = response.json().get("response", {}).get("docs", [])

            # 2. Fall back to base query if no keyword results
            if not docs:
                params["q"] = base_query
                response = requests.get(self._search_api, params=params, impersonate="chrome124", timeout=10)
                docs = response.json().get("response", {}).get("docs", [])

            if not docs:
                logger.debug(f"No results found for game title: {clean_title}")
                return None

            # 3. Score and select the best matching doc (filtering out soundtracks, manuals, etc.)
            best_doc = self._select_best_match(clean_title, docs)
            if best_doc:
                identifier = best_doc.get("identifier")
                logger.debug(f"Selected Internet Archive item for '{clean_title}': {identifier}")
                return f"https://archive.org/details/{identifier}"

            return None

        except Exception as e:
            logger.error(f"Internet Archive search error: {e}")
            return None

    def _select_best_match(self, query_title: str, docs: list[dict]) -> dict | None:
        """
        Scores search results to ensure we select an actual game release
        and avoid soundtracks, manuals, artbooks, or unrelated entries.
        """
        query_lower = query_title.lower()
        best_doc = None
        highest_score = -9999

        for doc in docs:
            title = doc.get("title", "").lower()
            score = 0

            # Exact or partial title match
            if query_lower == title:
                score += 50
            elif query_lower in title:
                score += 20

            # Heavy penalty for unwanted editions (soundtracks, manuals, guides, etc.)
            unwanted_keywords = ["soundtrack", "ost", "manual", "guide", "artbook", "book", "magazine", "trailer", "demo"]
            if any(kw in title for kw in unwanted_keywords):
                score -= 200

            # Reward game-related collections
            collections = doc.get("collection", [])
            if isinstance(collections, str):
                collections = [collections]

            if any(col in ["pc_games", "retrobytes", "softwarelibrary"] for col in collections):
                score += 30

            if score > highest_score:
                highest_score = score
                best_doc = doc

        # Fallback to first result if scores are heavily penalized but nothing better exists
        if highest_score > -500:
            return best_doc
        return docs[0] if docs else None

    @override
    def scrape_download_urls(self, game_url: str) -> dict[str, dict[str, str]]:
        """
        Given an archive.org details URL, fetches the file list from the metadata API
        and returns a dictionary of provider/file names and direct download URLs.
        """
        providers = {}
        try:
            # Extract identifier from URL (e.g. https://archive.org/details/my_game -> my_game)
            identifier = game_url.strip("/").split("/")[-1]

            meta_url = f"{self._metadata_api}/{identifier}"
            response = requests.get(meta_url, impersonate="chrome124", timeout=10)
            data = response.json()

            files = data.get("files", [])
            server = data.get("server", "")
            dir_path = data.get("dir", "")

            for file in files:
                name = file.get("name", "")

                # Filter for game archives, executables, or disk images
                if (
                    any(name.lower().endswith(ext) for ext in [".zip", ".rar", ".7z", ".iso", ".exe", ".cue", ".bin"])
                    and not any(ign in name.lower() for ign in ["sample", "readme", "patch"])
                    and not any(kw.lower() in name.lower() for kw in self.blocked_keywords)
                ):
                    direct_url = f"https://{server}{dir_path}/{name}"
                    providers[name] = direct_url

            logger.debug(f"Internet Archive providers: {providers}")
            return {"Internet Archive": providers}

        except Exception as e:
            logger.error(f"Internet Archive scrape error: {e}")
            return {}
