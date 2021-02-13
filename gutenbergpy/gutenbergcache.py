from __future__ import print_function
from gutenbergpy.parse.rdfparser import parse_rdf
from os import path
import time
from gutenbergpy.utils import Utils

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.caches.mongodbcache import MongodbCache

##
# Cache types
# noinspection PyClassHasNoInit


class GutenbergCacheTypes:
    CACHE_TYPE_SQLITE = 0
    CACHE_TYPE_MONGODB = 1


class GutenbergCache:
    """
    The main class (only this should be used to interface the cache)
    """

    @staticmethod
    def create(
        refresh=True,
        download=True,
        unpack=True,
        parse=True,
        cache=True,
        deleteTmp=False
    ):
        cache = MongodbCache()

        if path.isfile(GutenbergCacheSettings.CACHE_FILENAME) and refresh:
            print('Cache already exists')
            return

        if refresh:
            print('Deleting old files')
            Utils.delete_tmp_files(True)

        if download:
            Utils.download_file()

        if unpack:
            Utils.unpack_tarbz2()

        if parse:
            t0 = time.time()
            parse_rdf(cache)
            print('RDF PARSING took ' + str(time.time() - t0))

        if deleteTmp:
            print('Deleting temporary files')
            Utils.delete_tmp_files()

        print('Done')
