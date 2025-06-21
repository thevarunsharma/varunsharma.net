import requests
from urllib.parse import urlparse
from utils.scrape.base import BaseScraper


class MicrolinkScraper(BaseScraper):
    """
    A scraper that uses the Microlink API to fetch Open Graph metadata from a URL.
    This class is useful for extracting metadata such as title, description, image,
    site name, and locale from web pages that may not have Open Graph tags directly
    available or when you want to avoid scraping the page content directly.
    """

    def __init__(self, 
                 url):
        self.url = url
        self._data = self._fetch_data()

    def _fetch_data(self):
        response = requests.get("https://api.microlink.io/", params={"url": self.url})
        response.raise_for_status()
        json_data = response.json()

        if json_data.get("status") != "success":
            raise ValueError("Microlink API request failed.")

        return json_data.get("data", {})

    def get_og_title(self):
        return self._data.get("title")

    def get_og_locale(self):
        return self._data.get("lang")

    def get_og_description(self):
        return self._data.get("description")

    def get_og_image(self):
        return self._data.get("image", {}).get("url")

    def get_og_site_name(self):
        return self._data.get("publisher") or self._guess_site_name()

    def get_og_url(self):
        return self._data.get("url")

    def _guess_site_name(self):
        try:
            return urlparse(self._data.get("url", self.url)).hostname
        except:
            return None
