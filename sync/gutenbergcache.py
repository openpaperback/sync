from __future__ import print_function
from sync.parse.rdfparser import parse_rdf
import time
from sync.utils import Utils

from sync.caches.mongodbcache import MongodbCache


class GutenbergCache:
    """
    The main class (only this should be used to interface the cache)
    """

    @staticmethod
    def create(refresh=True, deleteTmp=False):

        if refresh:
            print('Deleting old files')
            Utils.delete_tmp_files()
            Utils.download_file()
            Utils.unpack_tarbz2()

        cache = MongodbCache()

        t0 = time.time()
        parse_rdf(cache)
        print('RDF PARSING took ' + str(time.time() - t0))

        if deleteTmp:
            print('Deleting temporary files')
            Utils.delete_tmp_files()

        print('Done')
