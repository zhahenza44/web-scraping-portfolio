# Web Scraping Portfolio

## Skill & Tools

- **Scrapy 2.19** — framework scraping Python
- **Playwright / scrapy-playwright** — render halaman JavaScript di browser
- **CSS / XPath selector** — ekstraksi data dari HTML
- **API JSON** — mengambil endpoint API publik
- **Data pipeline** — pembersihan data sebelum disimpan

## Contoh Project

### 1. Quotes Scraper — HTML Statis
- **File:** `jobscraper/jobscraper/spiders/quotes.py`
- **Target:** quotes.toscrape.com
- **Sumber data:** HTML statis
- **Hasil:** 100 quotes (10 halaman, pagination otomatis) dengan text, author, tags

### 2. Books Scraper — Pagination
- **File:** `jobscraper/jobscraper/spiders/books.py`
- **Target:** books.toscrape.com
- **Sumber data:** HTML + pagination 50 produk/halaman
- **Hasil:** 1000 buku (title, price, rating) — harga dibersihkan dari simbol mata uang

### 3. Hacker News Scraper — API JSON
- **File:** `jobscraper/jobscraper/spiders/hackernews.py`
- **Target:** hn.algolia.com (API Hacker News)
- **Sumber data:** JSON API (tanpa HTML)
- **Hasil:** 20 item trending (title, url, points, author)

### 4. JS Quotes Scraper — Playwright / Render Browser
- **File:** `jobscraper/jobscraper/spiders/jsquotes.py`
- **Target:** quotes.toscrape.com/js/ 
- **Sumber data:** browser via Playwright
- **Hasil:** 10 quotes

### Catatan Scrapy 2.19
Scrapy versi 2.19 menggunakan `async def start()` (bukan `start_requests()`). Spiders di repo ini sudah mengikuti API terbaru.

## Layanan yang Ditawarkan

- Scraping harga & katalog produk e-commerce
- Scraping data lowongan kerja / properti
- Monitoring data berkala (per hari/jam)
- Pembersihan & penyimpanan data (CSV/Excel/JSON)

**Kontak:** zhahenza@gmail.com
