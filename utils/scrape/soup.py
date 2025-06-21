import urllib.request
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utils.scrape.base import BaseScraper


class SoupScraper(BaseScraper):

    def __init__(self,
                 url):
        super().__init__(url)
        response = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(
            response, 
            'html.parser', 
            from_encoding=response.info().get_param('charset')
        )

    def get_og_title(self):
        if og_title := self.soup.findAll("meta", property="og:title"):
            return og_title[0]["content"]
        return

    def get_og_locale(self):
        if og_locale := self.soup.findAll("meta", property="og:locale"):
            return og_locale[0]["content"]    
        return

    def get_og_description(self):
        if og_description := self.soup.findAll("meta", property="og:description"):
            return og_description[0]["content"]
        return
    
    def get_og_site_name(self):
        if og_site_name := self.soup.findAll("meta", property="og:site_name"):
            return og_site_name[0]["content"]
        elif og_url := (self.get_og_url() or self.url):
            return urlparse(og_url).netloc
        return
    
    def get_og_image(self):
        if og_image := self.soup.findAll("meta", property="og:image"):
            return og_image[0]["content"]
        return

    def get_og_url(self):
        if og_url := self.soup.findAll("meta", property="og:url"):
            return og_url[0]["content"]    
        return
