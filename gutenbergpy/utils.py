import asyncio
import time
import sys
import os
import requests
import tarfile

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings


class Utils:

    @staticmethod
    def delete_tmp_files(delete_sqlite=False):
        """
        Deletes the temp files resulted in the cache process
        """

        if delete_sqlite:
            try:
                os.remove(GutenbergCacheSettings.CACHE_FILENAME)
            except OSError:
                pass
        try:
            os.remove(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME)
        except OSError:
            pass
        try:
            for root, dirs, files in os.walk(GutenbergCacheSettings.CACHE_RDF_UNPACK_DIRECTORY, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
        except OSError:
            pass

    @staticmethod
    def update_progress_bar(type: str):
        """
        used to update the progress bar display
        """
        sys.stdout.write(f'\r {type} ')
        sys.stdout.flush()

    @staticmethod
    def download_file():
        """
        used to download the rdf tar file
        """

        start = time.time()

        r = requests.get(GutenbergCacheSettings.CACHE_RDF_DOWNLOAD_LINK)
        with open(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME, 'wb') as output_file:
            output_file.write(r.content)

        print('took %f' % (time.time() - start))

    @staticmethod
    def unpack_tarbz2():
        """
        used to unpack the rdf tar file
        """

        start = time.time()
        tar = tarfile.open(GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME)
        type = 'Extracting  %s' % GutenbergCacheSettings.CACHE_RDF_ARCHIVE_NAME
        for idx, member in enumerate(tar.getmembers()):
            print(type, idx)
            tar.extract(member)
        tar.close()

        print('took %f' % (time.time() - start))


def background(f):
    from functools import wraps

    @wraps(f)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        if callable(f):
            return loop.run_in_executor(None, f, *args, **kwargs)
        else:
            raise TypeError('Task must be a callable')
    return wrapped
