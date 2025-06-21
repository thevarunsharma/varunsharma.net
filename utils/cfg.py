import logging
import os
import yaml
from utils.scrape import (
    MicrolinkScraper,
    SoupScraper
)
from concurrent.futures import ThreadPoolExecutor, as_completed
from diskcache import Cache

log = logging.getLogger(__name__)
PATH = os.environ.get("WEBAPP_CFG", "config.yaml")
cache = Cache("tmp")


def get_configs():
    with open(PATH, "r") as fh:
        configs = yaml.safe_load(fh)
    return configs


def get_post_meta(post):
    """Extract metadata for a single post.
    Parameters
    ----------
    post : dict
        A dictionary containing post metadata
    Returns
    -------
    dict
        A dictionary containing the post metadata, including title, locale,
        description, image, site_name, link, and captcha status.
    """
    post = post.copy()  # Avoid modifying the original post
    link = post.get("link", "#")
    captcha = post.get("captcha", False)
    try:
        scraper = MicrolinkScraper(link) if captcha else SoupScraper(link)
    except Exception as e:
        log.exception(f"Some error occurred while scraping {link}.\n{e}")
        return post
    post['title'] = post.get("title", scraper.get_og_title())
    post['locale'] = post.get("locale", scraper.get_og_locale())
    post['description'] = post.get("description", scraper.get_og_description())
    post["image"] = post.get("image", scraper.get_og_image())
    post["site_name"] = post.get("site_name", scraper.get_og_site_name())
    post["link"] = scraper.get_og_url()
    log.debug(post)
    return post


@cache.memoize(expire=604800, tag="post_meta")
def extract_post_meta(configs):
    posts = configs.get("posts", [])
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(get_post_meta, post): post for post in posts}
        for i, future in enumerate(as_completed(futures)):
            posts[i] = future.result()

    configs["posts"] = posts
    log.debug(f"Extracted metadata for {len(posts)} posts.")
    return configs
