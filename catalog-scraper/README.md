# Catalog Scraper — 1.000 Buku ke CSV

Scraper ringan tanpa framework: `httpx` + `lxml` + modul `csv` bawaan Python.
Target latihan resmi: `books.toscrape.com` (50 halaman x 20 buku).

## Cara jalan

```bash
python scrape_books.py
```

## Hasil

- `buku.csv` — 1.000 baris (judul, harga, rating, stok), UTF-8, siap buka di Excel/LibreOffice
- Pagination otomatis ikuti tombol "next" sampai halaman terakhir
- Rating kata ("Three") dinormalisasi jadi angka (3)
- Jeda 0,5 detik antar request (sopan ke server)
