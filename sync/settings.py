import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URL = "mongodb://127.0.0.1:27017"

    CACHE_DOWNLOAD_LINK = 'https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2'
    CACHE_UNPACK_DIRECTORY = os.path.join(os.getcwd(), 'cache')
    CACHE_ARCHIVE_NAME = 'rdf-files.tar.bz2'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
