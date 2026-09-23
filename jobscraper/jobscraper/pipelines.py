# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CleanQuotesPipeline:
    """Bersihkan data sebelum disimpan (pola untuk semua proyek)."""

    def process_item(self, item):
        adapter = ItemAdapter(item)
        if "text" in adapter:
            adapter["text"] = adapter["text"].strip().strip("\u201c\u201d")
        if "author" in adapter:
            adapter["author"] = adapter["author"].strip()
        if "tags" in adapter:
            adapter["tags"] = [t.strip() for t in adapter["tags"]]
        return item


class CleanDataPipeline:
    """Bersihkan data generik: harga 'Â£51.77' → '51.77', rating 'star-rating Three' → 'Three'."""

    def process_item(self, item):
        adapter = ItemAdapter(item)
        if "price" in adapter and adapter["price"]:
            adapter["price"] = adapter["price"].replace("\u00a3", "").replace("\u00c2", "").strip()
        if "rating" in adapter and adapter["rating"]:
            adapter["rating"] = adapter["rating"].replace("star-rating", "").strip()
        return item