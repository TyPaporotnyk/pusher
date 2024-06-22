from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db.models import QuerySet

from apps.posts.models import Post


@dataclass(frozen=True)
class BasePostService(ABC):

    @abstractmethod
    def get_all(self) -> QuerySet[Post]: ...

    @abstractmethod
    def get_by(self, **filters) -> QuerySet[Post]: ...


@dataclass(frozen=True)
class PostService(BasePostService):

    def get_all(self) -> QuerySet[Post]:
        return Post.objects.all().prefetch_related("images")

    def get_by(self, **filters) -> QuerySet[Post]:
        return Post.objects.filter(**filters).prefetch_related("images")
