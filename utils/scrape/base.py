from abc import ABC, abstractmethod


class BaseScraper(ABC):

    def __init__(self, url: str):
        self.url = url
        super().__init__()

    @abstractmethod
    def get_og_title(self):
        pass

    @abstractmethod
    def get_og_locale(self):
        pass

    @abstractmethod
    def get_og_description(self):
        pass

    @abstractmethod
    def get_og_site_name(self):
        pass

    abstractmethod
    def get_og_image(self):
        pass

    @abstractmethod
    def get_og_url(self):
        pass
