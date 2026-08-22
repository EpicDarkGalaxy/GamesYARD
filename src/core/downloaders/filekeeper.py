from curl_cffi import requests

from ..tools.utils import parseHtml
from .base import BaseDownloader


class FileKeeperDownloader(BaseDownloader):
    def can_handle(self, url: str) -> bool:
        return "filekeeper.net" in url

    def get_method(self) -> object:
        return self.extract_dl_url

    def extract_dl_url(self, landing_page_url) -> str | None:
        # 1. Fetch the landing page
        soup = parseHtml(landing_page_url)

        # 2. Find the countdown element
        countdown_element = soup.select_one("#download-countdown")
        if not countdown_element:
            return None

        # 3. Extract the variables directly from the data attributes
        code = countdown_element.get("data-code")
        referer = countdown_element.get("data-referer", "")
        rand = countdown_element.get("data-rand")
        method = countdown_element.get("data-method", "Free download")

        # 4. Prepare the POST payload
        payload = {
            "op": "download2",
            "id": code,
            "rand": rand,
            "referer": referer,
            "method_free": method,
            "down_direct": "1",
        }

        # 5. Perform the POST request to the same URL
        # We use the same 'scraper' session to keep cookies intact
        post_response = requests.post(
            landing_page_url, data=payload, impersonate="chrome124", stream=True
        )

        # print(f"Status: {post_response.status_code}")
        # print(f"Headers: {post_response.headers}")
        print(f"Response URL: {post_response.url}")
        # print(f"Content Type: {post_response.headers.get('Content-Type')}")

        post_response.close()
        return post_response.url

        # # If the server is sending you the file (binary), abort immediately!
        # if post_response.headers.get('Content-Type') == 'application/x-rar-compressed':
        #     print("Error: The server is sending the file, not the redirect/page!")
        #     return None

        # # 6. Look for the file URL in the POST response
        # # Often, the response HTML contains the final download link
        # post_soup = BeautifulSoup(post_response.text, 'html.parser')
        # final_link = post_soup.select_one("a.download-link") # Change this selector to match site

        # return final_link['href'] if final_link else None
