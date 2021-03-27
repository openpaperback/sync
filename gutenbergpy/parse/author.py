
class Author:
    """
    Used to hold an author in parse results after parsing
    """

    def __init__(
        self,
        gutenberg_id,
        aliases
    ):
        self.gutenberg_id = gutenberg_id
        self.aliases = aliases

    def to_dict(self):
        return {
            'gutenberg_id': self.gutenberg_id,
            'aliases': self.aliases,
        }
