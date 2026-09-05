import requests
from bs4 import BeautifulSoup

from src.core.utils.log import get_logger

logger = get_logger(__name__)

_STEAM_SEARCH_URL = "https://store.steampowered.com/api/storesearch/"
_STEAM_DETAILS_URL = "https://store.steampowered.com/api/appdetails"

_TAG_MAP = {
    "os": "OS",
    "operating system": "OS",
    "processor": "CPU",
    "cpu": "CPU",
    "memory": "RAM",
    "ram": "RAM",
    "graphics": "GPU",
    "video card": "GPU",
    "gpu": "GPU",
    "directx": "DirectX",
    "storage": "Storage",
    "hard drive": "Storage",
    "hard disk space": "Storage",
}


def _parse_steam_requirements_html(html: str) -> dict[str, str]:
    """Parses Steam's <ul><li>OS: ...</li></ul> requirement block into a clean tag->value dict."""
    if not html:
        return {}

    soup = BeautifulSoup(html, "html.parser")
    specs: dict[str, str] = {}

    for li in soup.select("li"):
        text = li.get_text(separator=" ", strip=True)
        if ":" not in text:
            continue
        label, _, value = text.partition(":")
        key = _TAG_MAP.get(label.strip().lower())
        if key and value.strip():
            specs[key] = value.strip()

    return specs


def get_steam_system_requirements(game_title: str) -> dict:
    """
    Standalone helper: searches Steam's storefront for a game title, then fetches
    and parses its official PC system requirements (minimum + recommended).

    Uses Steam's public storefront API (no key required). Returns the same shape
    expected by GameDetailsView.populate_requirements:
        {"requirements": {"minimum": {...}, "recommended": {...}}}
    """
    try:
        search_resp = requests.get(
            _STEAM_SEARCH_URL,
            params={"term": game_title, "cc": "us", "l": "en"},
            timeout=5,
        )
        search_resp.raise_for_status()
        items = search_resp.json().get("items", [])
        if not items:
            logger.info(f"No Steam store match found for: {game_title}")
            return {}

        app_id = items[0]["id"]

        details_resp = requests.get(
            _STEAM_DETAILS_URL,
            params={"appids": app_id, "cc": "us", "l": "en"},
            timeout=5,
        )
        details_resp.raise_for_status()
        payload = details_resp.json().get(str(app_id), {})

        if not payload.get("success"):
            logger.warning(f"Steam appdetails lookup failed for app_id: {app_id}")
            return {}

        data = payload.get("data", {})
        pc_reqs = data.get("pc_requirements", {})

        # Steam sometimes returns an empty list `[]` instead of a dict when there are no requirements at all
        if not isinstance(pc_reqs, dict):
            pc_reqs = {}

        minimum = _parse_steam_requirements_html(pc_reqs.get("minimum", ""))
        recommended = _parse_steam_requirements_html(pc_reqs.get("recommended", ""))

        logger.info(f"Fetched Steam system requirements for '{game_title}' (app_id={app_id})")
        return {
            "id": app_id,
            "game": data.get("name"),
            "requirements": {
                "minimum": minimum,
                "recommended": recommended,
            },
        }

    except requests.RequestException as e:
        logger.error(f"Steam system requirements fetch failed for '{game_title}': {e}")
        return {}
