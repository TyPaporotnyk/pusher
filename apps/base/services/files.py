import hashlib
import os
import tempfile

import requests
from django.core.files import File

from apps.base.exceptions.files import DownloadFileException


def download_file(url) -> tuple[str, File]:
    response = requests.get(url, stream=True)
    if response.status_code != requests.codes.ok:
        raise DownloadFileException

    hash_object = hashlib.md5(url.encode())
    file_extension = os.path.splitext(url)[-1]
    file_name = f"{hash_object.hexdigest()[:10]}{file_extension}"

    lf = tempfile.NamedTemporaryFile(delete=False)

    for block in response.iter_content(1024 * 8):
        if not block:
            break

        lf.write(block)

    lf.seek(0)
    return file_name, File(lf)
