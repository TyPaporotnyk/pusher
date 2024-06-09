from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db.models import QuerySet

from apps.customers.models import Customer
from apps.posts.models import Post


@dataclass(kw_only=True)
class BaseCustomerPostsFilter(ABC):
    customer: Customer

    @abstractmethod
    def get_filtered_posts(self, posts: QuerySet[Post]) -> list[Post]: ...

    @abstractmethod
    def _check_post_by_keyword(self, post: Post) -> bool: ...

    @abstractmethod
    def _check_post_by_groups(self, post: Post) -> bool: ...

    @abstractmethod
    def _check_post_by_blacklist(self, post: Post) -> bool: ...
