import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    CACHE_RDF_DOWNLOAD_LINK = 'https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2'
    CACHE_RDF_UNPACK_DIRECTORY = os.path.join('cache', "epub")
    CACHE_RDF_ARCHIVE_NAME = 'rdf-files.tar.bz2'
    TEXT_FILES_CACHE_FOLDER = 'texts'
    MONGO_DB_CONNECTION_SERVER = "mongodb://172.17.16.1:27017"

    NS = {
        'cc': "http://web.resource.org/cc/",
        'dcam': "http://purl.org/dc/dcam/",
        'dcterms': "http://purl.org/dc/terms/",
        'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'pgterms': "http://www.gutenberg.org/2009/pgterms/"
    }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
