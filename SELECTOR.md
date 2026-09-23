# SELECTOR.md — Panduan Cepat CSS/XPath untuk Scrapy (Esensial)

Milik: zhahenza | Tujuan: portofolio freelance scraping semua kategori

## 1. Logika dasar membaca HTML (5 menit)

Halaman web = HTML, struktur "kotak dalam kotak":

```html
<div class="quote">            <- container 1 listing
  <span class="text">"Kata-kata"</span>
  <small class="author">Nama Author</small>
  <a href="/tag/xxx">tag</a>
</div>
```

- **Tag**: `div`, `span`, `a`, `h1`... = jenis elemen
- **Class** (`class="quote"`): label penanda, boleh sama di banyak elemen
- **ID** (`id="main"`): label unik, hanya satu
- **Attribute**: `href`, `src`, `title`... = properti tambahan

Tri: di browser, klik kanan elemen → **Inspect** → lihat struktur langsung.

## 2. CSS Selector (paling umum dipakai)

| Sintaks | Arti | Contoh |
|---|---|---|
| `element` | pilih tag | `h2` |
| `.class` | pilih class | `.quote` |
| `#id` | pilih id | `#main` |
| `a::text` | ambil TEKS dari link | `small.author::text` |
| `a::attr(href)` | ambil ATTRIBUTE | `a::attr(href)` |
| `.get()` | ambil SATU hasil pertama | `sel.css("h2::text").get()` |
| `.getall()` | ambil SEMUA hasil | `sel.css(".text::text").getall()` |

Cara pakai di Scrapy:
```python
response.css("small.author::text").getall()
response.css("li.next a::attr(href)").get()
```

## 3. XPath (mirip, kadang lebih kuat utk pola kompleks)

| Sintaks | Arti |
|---|---|
| `//tag` | semua tag di mana saja |
| `//tag[@class='x']` | tag yang class-nya x |
| `/text()` | teks |
| `/@attr` | attribute |
| `.//x` | relatif dari posisi saat ini |

Contoh:
```python
response.xpath("//small[@class='author']/text()").getall()
response.xpath("//li[@class='next']/a/@href").get()
```

## 4. Kapan pakai CSS vs XPath?

- **CSS**: 90% kebutuhan harian, ringkas, jelas
- **XPath**: untuk pola kompleks (parent/child relatif, kondisi)
- Boleh **campur**: `.css(...)` lalu `.xpath(...)` bertumpuk

## 5. Selector "universal" yang kita pelajari (berlaku semua kategori)

Pola dasar yang sama untuk tips: listing → detail → pagination

| Bagian | CSS | XPath |
|---|---|---|
| Semua item container | `.item` | `//div[@class='item']` |
| Judul item | `h2 a::text` | `//h2/a/text()` |
| Link detail | `h2 a::attr(href)` | `//h2/a/@href` |
| Tombol next | `li.next a::attr(href)` | `//li[@class='next']/a/@href` |

## 6. Kesalahan umum & trik

1. **Selector kosong / None** → cek penulisan class (Enter pengejaan: `.author` vs `.aurthor`), cek apakah elemen benar di halaman.
2. **`.get()` vs `.getall()`** — get = 1, getall = list.
3. **Selector ganda hasil** → selalu gunakan `.getall()` lalu ambil index.
4. **Order penting** — Scrapy memproses dari kiri ke kanan: `.css(".quote").css("span::text")` = text dari span DI DALAM quote.
5. **Debug cepat**: `scrapy shell "URL"` lalu ketik selector live di terminal.
6. **Format bersih**: `.strip()` untuk hilangkan spasi, `.re_first(r"\d+")` untuk ambil angka.

## 7. Latihan mandiri level Minggu 1

Di situs `quotes.toscrape.com` ambil lewat `scrapy shell`:
1. Semua teks quote → `.css("span.text::text").getall()`
2. Semua author → `.css("small.author::text").getall()`
3. Link "Next" → `.css("li.next a::attr(href)").get()`
4. Tag pertama dari quote #1 → coba sendiri!
5. Total quote yang tampil di halaman 1

## 8. API JSON di balik halaman JS (Skill Minggu 4 — harga jual naik)

### Kenapa penting
Situs modern (React/SPA) seringmu data dengan JavaScript: HTML mentah-nya kosong (0 quote!), tapi data ASLI ada di request API JSON di balik layar. Scrapy unggul karena **langsung memanggil API itu** — lebih cepat & stabil daripada menonton browser render.

### Cara menemukan API (lewat browser, 4 langkah)
1. Buka situs target di browser
2. Tekan **F12** (DevTools) → tab **Network**
3. Reload halaman (Ctrl+R)
4. Filter request: pilih tab **Fetch/XHR** → cari response berisi JSON → salin URL-nya

### Cara memanggil di Scrapy (tanpa CSS selector)
```python
import scrapy, json

class ApiSpider(scrapy.Spider):
    name = "api"
    start_urls = ["https://HASIL_PENEMUANMU"]  # URL API JSON

    def parse(self, response):
        data = json.loads(response.text)
        for item in data.get("hits", []):
            yield {
                "title": item.get("title"),
                "url": item.get("url"),
                "points": item.get("points"),
            }
```
Bedanya dengan sekolah-sekolah sebelumnya: tidak ada `.css()`, karena datanya **JSON** (bukan HTML) — pakai `json.loads(response.text)` + `data.get("key")`.

### Contoh nyata yang sudah dikerjakan
- API: `https://hn.algolia.com/api/v1/search?tags=front_page` (Hacker News)
- Ambil: title, url, points, author → `hackernews.csv` (20 item, hidup)
- Coba: ketik URL di browser → tidak tampil di HTML → tapi di Network tab jadi JSON besar

### 3 cara data muncul di web (peta mental)
| Cara | Datanya tinggal di | Tools | Status kamu |
|---|---|---|---|
| HTML statis | di HTML | Scrapy biasa | ✅ quotes, books |
| API JSON | di luar HTML, dipanggil JS | Scrapy `json.loads` | ✅ hackernews (baru) |
| Browser rendering | diproduksi JS browser | Playwright | 🔜 pelajaran lanjutan |

### Trik tambahan
- API sering butuh **parameter pagination** (`page=2`) atau **filter** — tambahkan di URL.
- Kalau data 1 API tidak lengkap, biasanya ada **beberapa API** (detail per item) — follow link seperti pagination.
- Selalu cek **robots.txt** & ToS target — SOP freelance.
## §9 Playwright — render JS di browser (Minggu 5)

### Kenapa butuh Playwright
Situs seperti `quotes.toscrape.com/js/` **menyembunyikan data**: HTML mentahnya kosong/kecil, data dibuat oleh JavaScript di browser setelah halaman dibuka. Scrapy biasa cuma dapat HTML mentah (5886 byte, 0 quote). Browser sungguhan = data jadi (10 quote).

### Setup
```bash
pip install playwright scrapy-playwright
python3 -m playwright install --with-deps chromium   # butuh sudo sekali
```

### Config di `settings.py`
```python
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}
```

### Spider dengan browser
```python
import scrapy
from scrapy_playwright.page import PageMethod

class JsQuotesSpider(scrapy.Spider):
    name = "jsquotes"
    start_urls = ["https://quotes.toscrape.com/js/"]

    async def start(self):          # API BARU Scrapy 2.19 (bukan start_requests!)
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
```

### PENTING: Scrapy 2.19 menghapus `start_requests()`
- Pakai `async def start(self): yield ...` — bukan `def start_requests(self): yield ...`.
- Kalau spider mendefinisikan `start_requests`, engine **tak pernah memanggilnya** → 0 hasil.
- Spider lama (quotes/books) tetap jalan karena hanya pakai `start_urls` (default `start()`).
- Tanda sukses: log `Crawled (200) <...> ['playwright']` dan `item_scraped_count` > 0.
- Format page method TIDAK pakai dict; wajib kelas `PageMethod("nama_method", *args)`.
- `mplay method`: untuk halaman yang menunggu data, pakai `wait_for_selector`.

### Hasil nyata
- `jsquotes.py` → `jsquotes.csv`: 10 quote dari halaman yang HTML mentahnya 0 quote.
