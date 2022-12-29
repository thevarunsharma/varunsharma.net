import logging
import os
import yaml
from .scrape import Scraper

log = logging.getLogger(__name__)
PATH = os.environ.get("WEBAPP_CFG", "config.yaml")

def get_configs():
    with open(PATH, "r") as fh:
        configs = yaml.safe_load(fh)
    return configs


def extract_post_meta(configs):
    posts = configs.get("posts", {})

    for post in posts:
        link = post.get("link", "#")
        try:
            scraper = Scraper(link)
            post['title'] = post.get("title", scraper.get_og_title())
            post['locale'] = post.get("locale", scraper.get_og_locale())
            post['description'] = post.get("description", scraper.get_og_description())
            post["image"] = post.get("image", scraper.get_og_image())
            post["site_name"] = post.get("site_name", scraper.get_og_site_name())
            post["link"] = scraper.get_og_url()
        except Exception as e:
            log.exception(f"Some error occured while scraping {link}.\n{e}")
    
    return configs
        

