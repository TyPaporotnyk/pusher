from contextlib import contextmanager

from django.conf import settings
from mysql.connector import connect


@contextmanager
def get_connection():
    with connect(
        user=settings.DB_EXTERNAL_USER,
        password=settings.DB_EXTERNAL_PASSWORD,
        host=settings.DB_EXTERNAL_HOST,
        port=settings.DB_EXTERNAL_PORT,
        database=settings.DB_EXTERNAL_NAME,
    ) as session:
        yield session
