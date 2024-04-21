from datetime import datetime

from pydantic import BaseModel


class FacebookBase(BaseModel):
    id: int
    post_id: int
    post_link: str
    actor_name: str
    actor_link: str | None
    creation_time: datetime
    message: str
    attachments: list[str]
    tags: str


class FacebookGroup(FacebookBase):
    group_name: str
    group_link: str


class FacebookKeyword(FacebookBase):
    key: str
    key_link: str
