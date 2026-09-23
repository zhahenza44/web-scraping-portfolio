import scrapy
from scrapy_playwright.page import PageMethod


class JsQuotesSpider(scrapy.Spider):
    name = "jsquotes"
    start_urls = ["https://quotes.toscrape.com/js/"]

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div.quote", timeout=15000)
                    ],
                },
            )

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }