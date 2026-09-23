import scrapy

from jobscraper.items import BooksItem


class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            yield BooksItem(
                title=book.css("h3 a::text").get(),
                price=book.css("p.price_color::text").get(),
                rating=book.css("p.star-rating::attr(class)").get(),
                link=book.css("h3 a::attr(href)").get(),
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)