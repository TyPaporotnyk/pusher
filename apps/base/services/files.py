import tempfile

import requests
from django.core import files

from apps.base.exceptions.files import DownloadFileException


def download_file(url) -> tuple[str, files.File]:
    response = requests.get(url, stream=True)
    if response.status_code != requests.codes.ok:
        raise DownloadFileException

    file_name = url.split("/")[-1]
    lf = tempfile.NamedTemporaryFile()

    for block in response.iter_content(1024 * 8):
        if not block:
            break

        lf.write(block)

    return file_name, files.File(lf)
