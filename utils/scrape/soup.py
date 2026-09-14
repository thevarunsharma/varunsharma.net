import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utils.scrape.base import BaseScraper


class SoupScraper(BaseScraper):

    def __init__(self,
                 url):
        super().__init__(url)
        request = urllib.request.Request(
            self.url,
            headers={"User-Agent": "varunsharma.net-generator/1.0"},
        )
        response = urllib.request.urlopen(request, timeout=15)
        self.soup = BeautifulSoup(
            response, 
            'html.parser', 
            from_encoding=response.info().get_param('charset')
        )

    def _meta_content(self, *names):
        for name in names:
            for attr in ("property", "name"):
                tag = self.soup.find("meta", attrs={attr: name})
                if tag and tag.get("content"):
                    return tag["content"].strip()
        return None

    def get_og_title(self):
        return self._meta_content("og:title", "twitter:title") or self._page_title()

    def get_og_locale(self):
        return self._meta_content("og:locale")

    def get_og_description(self):
        return self._meta_content("og:description", "twitter:description", "description")
    
    def get_og_site_name(self):
        return self._meta_content("og:site_name") or urlparse(self.get_og_url() or self.url).netloc
    
    def get_og_image(self):
        return self._meta_content("og:image", "twitter:image", "twitter:image:src")

    def get_og_url(self):
        return self._meta_content("og:url") or self.url

    def _page_title(self):
        if self.soup.title and self.soup.title.string:
            return self.soup.title.string.strip()
        return None
