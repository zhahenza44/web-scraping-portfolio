from dataclasses import dataclass, field


@dataclass
class QuotesItem:
    text: str = ""
    author: str = ""
    tags: list = field(default_factory=list)


@dataclass
class BooksItem:
    title: str = ""
    price: str = ""
    rating: str = ""
    link: str = ""