class BaseScraper:
    def __init__(self) -> None:
        pass

    def find_game_url(self, game_title: str) -> str | None:
        raise NotImplementedError

    def scrape_download_urls(self, game_url: str) -> dict[str, dict[str, str]]:
        raise NotImplementedError
