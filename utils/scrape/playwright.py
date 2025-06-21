import asyncio
from utils.scrape.base import BaseScraper
from playwright.async_api import async_playwright


class PlaywrightScraper(BaseScraper):
    def __init__(self,
                 url):
        super().__init__(url)
        self._og_data = {}
        self.load()

    def load(self):
        """Sync wrapper that runs the async loader."""
        asyncio.run(self._async_load())

    async def _async_load(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto(self.url, timeout=60000)

            # Wait for OG tags (if they’re rendered dynamically)
            try:
                await page.wait_for_selector('meta[property^="og:"]', timeout=5000)
            except:
                pass  # still try to extract

            # Optional: wait a bit to allow JS-rendered tags to load
            await asyncio.sleep(1.5)

            # Extract OG tags
            self._og_data = await page.eval_on_selector_all(
                'meta[property^="og:"]',
                '''elements => Object.fromEntries(
                    elements.map(e => [e.getAttribute("property"), e.getAttribute("content")])
                )'''
            )

            await browser.close()

    def get_og_title(self):
        return self._og_data.get("og:title")

    def get_og_locale(self):
        return self._og_data.get("og:locale")

    def get_og_description(self):
        return self._og_data.get("og:description")

    def get_og_image(self):
        return self._og_data.get("og:image")

    def get_og_site_name(self):
        return self._og_data.get("og:site_name")

    def get_og_url(self):
        return self._og_data.get("og:url")
