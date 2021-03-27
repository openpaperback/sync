import re
from os import listdir, path
from typing import List

from lxml import etree
from sync.caches.mongodbcache import MongodbCache
from sync.parse.author import Author
from sync.parse.book import Book
from sync.parse.parsers import (parse_author, parse_author_id,
                                parse_bookshelves, parse_date_issued,
                                parse_downloads, parse_formats,
                                parse_languages, parse_publisher, parse_rights,
                                parse_subjects, parse_title, parse_type)
from sync.settings import settings
from sync.utils import Utils


def parse_rdf(db: MongodbCache):
    files = [d for d in listdir(settings.CACHE_UNPACK_DIRECTORY) if d.startswith("pg") and d.endswith(".rdf")]
    total = len(files)

    for index, file_name in enumerate(files):
        file_name_stripped = re.search("pg(.*?).rdf", file_name).group(1)

        Utils.update_progress_bar(f"Processing progress: {index} / {total}")
        file_path = path.join(settings.CACHE_UNPACK_DIRECTORY, file_name)
        doc = etree.parse(file_path, etree.ETCompatXMLParser())

        gutenberg_book_id = int(file_name_stripped)
        author_aliases = parse_author(doc)
        gutenberg_author_id = parse_author_id(doc)

        newbook = Book(
            gutenberg_id=gutenberg_book_id,
            number_of_downloads=parse_downloads(doc),
            date_issued=parse_date_issued(doc),
            title=parse_title(doc),
            doc_type=parse_type(doc),
            language=parse_languages(doc),
            author=author_aliases,
            gutenberg_author_id=gutenberg_author_id,
            formats=parse_formats(doc),
            publisher=parse_publisher(doc),
            rights=parse_rights(doc),
            subjects=parse_subjects(doc),
            bookshelves=parse_bookshelves(doc),
        )

        author = Author(
            gutenberg_id=gutenberg_author_id,
            aliases=author_aliases,
        )

        db.insert_book(newbook)
        db.insert_author(author)

    db.flush()
