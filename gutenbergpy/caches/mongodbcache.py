from gutenbergpy.parse.author import Author
from gutenbergpy.parse.book import Book
from gutenbergpy.settings import settings

import pymongo
from pymongo import MongoClient, UpdateOne


class MongodbCache():
    def __init__(self):
        self.limit = 500
        self.client = MongoClient(settings.MONGO_URL)

        self.db = self.client.gutenbooks
        self.db.books.create_index([('gutenberg_id', pymongo.ASCENDING)], unique=True)
        self.db.authors.create_index([('gutenberg_id', pymongo.ASCENDING)], unique=True)

        self.book_updates = []
        self.author_updates = []

    def clear_cache(self):
        self.db.books.drop()
        self.db.authors.drop()

    def try_commit_books(self):
        if(len(self.book_updates) >= self.limit):
            self.db.books.bulk_write(self.book_updates)
            self.book_updates = []

    def try_commit_authors(self):
        if(len(self.author_updates) >= self.limit):
            self.db.authors.bulk_write(self.author_updates)
            self.author_updates = []

    def flush(self):
        self.db.books.bulk_write(self.book_updates)
        self.db.authors.bulk_write(self.author_updates)

    def insert_book(self, book: Book):
        self.book_updates.append(
            UpdateOne(
                {'gutenberg_id': book.gutenberg_id},
                {'$set': book.to_dict()},
                upsert=True
            )
        )
        self.try_commit_books()

    def insert_author(self, author: Author):
        self.author_updates.append(
            UpdateOne(
                {'gutenberg_id': author.gutenberg_id},
                {
                    '$set': {'gutenberg_id': author.gutenberg_id},
                    '$addToSet': {'aliases':  {'$each': author.aliases}},
                },
                upsert=True
            )
        )
        self.try_commit_authors()
