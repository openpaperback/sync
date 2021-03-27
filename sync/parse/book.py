
class Book:
    """
    Used to hold a book in parse results after parsing
    """

    def __init__(
        self,
        gutenberg_id,
        date_issued,
        number_of_downloads,
        title,
        doc_type,
        language,
        author,
        gutenberg_author_id,
        formats,
        publisher,
        rights,
        subjects,
        bookshelves,
    ):
        self.gutenberg_id = gutenberg_id
        self.date_issued = date_issued
        self.number_of_downloads = number_of_downloads
        self.title = title
        self.doc_type = doc_type
        self.language = language
        self.author = author
        self.gutenberg_author_id = gutenberg_author_id
        self.formats = formats
        self.publisher = publisher
        self.rights = rights
        self.subjects = subjects
        self.bookshelves = bookshelves

    def to_dict(self):
        return {
            'gutenberg_id': self.gutenberg_id,
            'date_issued': self.date_issued,
            'number_of_downloads': self.number_of_downloads,
            'title': self.title,
            'doc_type': self.doc_type,
            'language': self.language,
            'author': self.author,
            'gutenberg_author_id': self.gutenberg_author_id,
            'formats': self.formats,
            'publisher': self.publisher,
            'rights': self.rights,
            'subjects': self.subjects,
            'bookshelves': self.bookshelves,
        }
