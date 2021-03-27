from gutenbergpy.parse.author import Author
from gutenbergpy.parse.book import Book
from gutenbergpy.settings import settings
from gutenbergpy.settings import settings

import pymongo
from pymongo import MongoClient


class MongodbCache():
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URL)

        self.db = self.client.gutenbooks
        self.db.books.create_index([('gutenberg_id', pymongo.ASCENDING)], unique=True)
        self.db.authors.create_index([('gutenberg_id', pymongo.ASCENDING)], unique=True)

    def clear_cache(self):
        self.db.books.drop()
        self.db.authors.drop()

    def insert_book(self, book: Book):
        try:
            self.db.books.update_one(
                {'gutenberg_id': book.gutenberg_id},
                {'$set': book.to_dict()},
                upsert=True
            )
        except Exception as ex:
            pass

    def insert_author(self, author: Author):
        try:
            self.db.authors.update_one(
                {'gutenberg_id': author.gutenberg_id},
                {
                    '$set': {
                        'gutenberg_id': author.gutenberg_id
                    },
                    '$addToSet': {
                        'aliases':  {'$each': author.aliases}
                    },
                },
                upsert=True
            )
        except Exception as ex:
            pass
