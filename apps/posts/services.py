from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db.models import QuerySet

from apps.posts.models import Post
from apps.posts.repository import PostRepository


@dataclass(frozen=True)
class BasePostService(ABC):
    post_repository: PostRepository

    @abstractmethod
    def get_all_posts(self) -> QuerySet[Post]: ...


@dataclass(frozen=True)
class PostService(BasePostService):

    def get_all_posts(self) -> QuerySet[Post]:
        return self.post_repository.get_all().prefetch_related("images")
