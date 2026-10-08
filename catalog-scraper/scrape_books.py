"""Latihan Level 1: scrape 50 halaman books.toscrape.com -> buku.csv
Cara jalan: /home/zhahenza/Freelance/projek/scrapy-projects/.venv/bin/python scrape_books.py
"""
import csv
import time
from urllib.parse import urljoin

import httpx
from lxml import html

BASE = "https://books.toscrape.com/"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def scrape_page(client, url):
    resp = client.get(url, timeout=15)
    resp.raise_for_status()
    doc = html.fromstring(resp.text)
    rows = []
    for b in doc.cssselect("article.product_pod"):
        title = b.cssselect("h3 a")[0].get("title")
        price = b.cssselect(".price_color")[0].text_content().strip()
        rating_word = b.cssselect("p.star-rating")[0].get("class").split()[-1]
        rating = RATING_MAP.get(rating_word, "")
        stock = b.cssselect(".instock.availability")[0].text_content().strip()
        rows.append([title, price, rating, stock])
    next_links = doc.cssselect("li.next a")
    next_url = urljoin(url, next_links[0].get("href")) if next_links else None
    return rows, next_url


def main():
    all_rows = []
    url = BASE
    page = 1
    with httpx.Client(headers={"User-Agent": "latihan-scrape/1.0"}) as client:
        while url:
            rows, url = scrape_page(client, url)
            all_rows.extend(rows)
            print(f"Halaman {page}: {len(rows)} buku (total {len(all_rows)})", flush=True)
            page += 1
            time.sleep(0.5)
    with open("buku.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["judul", "harga", "rating", "stok"])
        w.writerows(all_rows)
    print(f"Selesai: {len(all_rows)} buku -> buku.csv")


if __name__ == "__main__":
    main()
