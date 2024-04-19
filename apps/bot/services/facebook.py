from dataclasses import dataclass

from mysql.connector.pooling import PooledMySQLConnection


@dataclass(frozen=True)
class FacebookRepository:
    session: PooledMySQLConnection

    def get_new_group_adverts(self, last_real_estate_id: int):
        with self.session.cursor() as cursor:
            query = (
                "SELECT distinct message , id, post_link, actor_link, attachment, group_name, group_link "
                "FROM groups_facebook "
                "WHERE id > %s "
                "order by id desc" % last_real_estate_id
            )
            cursor.execute(query)
            return cursor.fetchall()

    def get_new_keyword_adverts(self, last_real_estate_id: int):
        with self.session.cursor() as cursor:
            query = (
                "SELECT distinct message , id, post_link, actor_link, attachment, group_name, group_link "
                "FROM key_facebook "
                "WHERE id > %s "
                "order by id desc" % last_real_estate_id
            )
            cursor.execute(query)
            return cursor.fetchall()
