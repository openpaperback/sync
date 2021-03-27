from __future__ import print_function
from gutenbergpy.parse.rdfparser import parse_rdf
from os import path
import time
from gutenbergpy.utils import Utils

from gutenbergpy.caches.mongodbcache import MongodbCache


class GutenbergCache:
    """
    The main class (only this should be used to interface the cache)
    """

    @staticmethod
    def create(
        refresh=True,
        parse=True,
        cache=True,
        deleteTmp=False
    ):
        cache = MongodbCache()

        if refresh:
            print('Deleting old files')
            Utils.delete_tmp_files()
            Utils.download_file()
            Utils.unpack_tarbz2()

        if parse:
            t0 = time.time()
            parse_rdf(cache)
            print('RDF PARSING took ' + str(time.time() - t0))

        if deleteTmp:
            print('Deleting temporary files')
            Utils.delete_tmp_files()

        print('Done')
