from gutenbergpy.parse.book import Book
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings

import pymongo
from pymongo import MongoClient


class MongodbCache():
    def __init__(self):
        self.client = MongoClient(GutenbergCacheSettings.MONGO_DB_CONNECTION_SERVER)

        self.db = self.client.gutenbooks
        self.collection = self.db.books
        self.collection.create_index([('gutenberg_id', pymongo.ASCENDING)], unique=True)

    def clear_cache(self):
        self.collection.drop()

    def insert(self, book: Book):
        try:
            self.collection.update_one(
                {'gutenberg_id': book.gutenberg_id},
                {'$set': book.to_dict()},
                upsert=True
            )
        except Exception as ex:
            pass
