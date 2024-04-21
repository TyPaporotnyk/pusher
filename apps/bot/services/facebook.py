from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from apps.bot.entities import FacebookGroup, FacebookKeyword
from apps.bot.utils.session import get_connection


class FacebookBaseRepository(ABC):

    @abstractmethod
    def get_new_adverts(self, last_real_estate_id: int) -> list[Any]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _get_entity_from_raw_data(raw_data):
        raise NotImplementedError


@dataclass(frozen=True)
class FacebookGroupRepository(FacebookBaseRepository):

    @staticmethod
    def _get_entity_from_raw_data(raw_data: tuple) -> FacebookGroup:
        return FacebookGroup(
            id=raw_data[0],
            post_id=raw_data[1],
            post_link=raw_data[2],
            actor_name=raw_data[3],
            actor_link=raw_data[4],
            creation_time=raw_data[5],
            message=raw_data[6],
            attachments=raw_data[7].split(","),
            group_name=raw_data[8],
            group_link=raw_data[9],
            tags=raw_data[10],
        )

    def get_new_adverts(self, last_real_estate_id: int) -> list[FacebookGroup]:
        with get_connection() as session:
            with session.cursor() as cursor:
                query = (
                    "SELECT id, post_id, post_link, actor_name, actor_link, creation_time, "
                    "message, attachment, group_name, group_link, tags "
                    "FROM groups_facebook "
                    "WHERE id > %s "
                    "order by id desc" % last_real_estate_id
                )
                cursor.execute(query)
                return [self._get_entity_from_raw_data(raw_data) for raw_data in cursor.fetchall()]


@dataclass(frozen=True)
class FacebookKeywordRepository(FacebookBaseRepository):

    @staticmethod
    def _get_entity_from_raw_data(raw_data) -> FacebookKeyword:
        return FacebookKeyword(
            id=raw_data[0],
            post_id=raw_data[1],
            post_link=raw_data[2],
            actor_name=raw_data[3],
            actor_link=raw_data[4],
            creation_time=raw_data[5],
            message=raw_data[6],
            attachment=raw_data[7].split(","),
            key=raw_data[8],
            key_link=raw_data[9],
            tags=raw_data[10],
        )

    def get_new_adverts(self, last_real_estate_id: int) -> list[FacebookKeyword]:
        with get_connection() as session:
            with session.cursor() as cursor:
                query = (
                    "SELECT id, post_id, post_link, actor_name, actor_link, creation_time, "
                    "message, attachment, key, key_link, tags "
                    "FROM groups_facebook "
                    "WHERE id > %s "
                    "order by id desc" % last_real_estate_id
                )
                cursor.execute(query)
                return [self._get_entity_from_raw_data(raw_data) for raw_data in cursor.fetchall()]
