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
                [os.remove(os.path.join(root, name)) for name in files]
                [os.rmdir(os.path.join(root, name)) for name in dirs]
        except OSError:
            pass

    @staticmethod
    def update_progress_bar(message: str):
        """
        used to update the progress bar display
        """
        sys.stdout.write(f'\r {message} ')
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
        for index, member in enumerate(tar.getmembers()):
            Utils.update_progress_bar(f'Extracting {index}')
            member.name = os.path.basename(member.name)
            tar.extract(member, path=settings.CACHE_UNPACK_DIRECTORY)
        tar.close()

        print(f'took {time.time() - start}')
