from contextlib import contextmanager

from django.conf import settings
from mysql.connector import connect

from apps.bot.services.facebook import FacebookRepository


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


def get_new_group_adverts(last_id: int):
    with get_connection() as session:
        facebook_repository = FacebookRepository(session)

        new_group_adverts = facebook_repository.get_new_group_adverts(last_id)

        return new_group_adverts


def get_new_keyword_adverts(last_id: int):
    with get_connection() as session:
        facebook_repository = FacebookRepository(session)

        new_group_adverts = facebook_repository.get_new_keyword_adverts(last_id)

        return new_group_adverts
