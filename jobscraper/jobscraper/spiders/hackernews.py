import scrapy
import json


class HackerNewsSpider(scrapy.Spider):
    name = "hackernews"
    start_urls = ["https://hn.algolia.com/api/v1/search?tags=front_page"]

    def parse(self, response):
        data = json.loads(response.text)
        for item in data.get("hits", []):
            yield {
                "title": item.get("title"),
                "url": item.get("url"),
                "points": item.get("points"),
                "author": item.get("author"),
            }