import os
import sys
import tarfile
import time

import requests

from sync.settings import settings


class Utils:

    @staticmethod
    def delete_tmp_files():
        """
        Deletes the temp files resulted in the cache process
        """
        try:
            os.remove(settings.CACHE_ARCHIVE_NAME)
        except OSError:
            pass
        try:
            for root, dirs, files in os.walk(settings.CACHE_UNPACK_DIRECTORY, topdown=False):
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

        r = requests.get(settings.CACHE_DOWNLOAD_LINK)
        with open(settings.CACHE_ARCHIVE_NAME, 'wb') as output_file:
            output_file.write(r.content)

        print('Download took %f' % (time.time() - start))

    @staticmethod
    def unpack_tarbz2():
        """
        used to unpack the rdf tar file
        """

        start = time.time()
        tar = tarfile.open(settings.CACHE_ARCHIVE_NAME)
        type = 'Extracting  %s' % settings.CACHE_ARCHIVE_NAME
        for idx, member in enumerate(tar.getmembers()):
            print(type, idx)
            tar.extract(member)
        tar.close()

        print('took %f' % (time.time() - start))
