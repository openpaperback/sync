from gutenbergpy.parse.author import Author
from gutenbergpy.caches.mongodbcache import MongodbCache
from typing import List
from gutenbergpy.parse.parsers import parse_author, parse_author_id, parse_bookshelves, parse_date_issued, parse_downloads, parse_formats, parse_languages, parse_publisher, parse_rights, parse_subjects, parse_title, parse_type
from os import listdir
from os import path
from lxml import etree

from gutenbergpy.parse.book import Book
from gutenbergpy.settings import settings
from gutenbergpy.utils import Utils


def parse_rdf(db: MongodbCache):
    result: List[Book] = []

    dirs = [d for d in listdir(settings.CACHE_UNPACK_DIRECTORY) if not d.startswith("DELETE")]
    total = len(dirs)

    for index, dir in enumerate(dirs):
        processing_str = f"Processing progress: {index} / {total}"

        Utils.update_progress_bar(processing_str)
        file_path = path.join(settings.CACHE_UNPACK_DIRECTORY, dir, 'pg%s.rdf' % (dir))
        doc = etree.parse(file_path, etree.ETCompatXMLParser())

        gutenberg_book_id = int(dir)
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

    return result
