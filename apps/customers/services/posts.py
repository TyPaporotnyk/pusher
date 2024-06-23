import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from apps.common.models import Keyword
from apps.customers.models import Customer, CustomerPost
from apps.posts.models import Post

logger = logging.getLogger(__name__)


@dataclass
class BaseCustomerPostService(ABC):
    customer: Customer

    @abstractmethod
    def get(self, obj_id: int) -> CustomerPost: ...

    @abstractmethod
    def get_all(self, **filter_by) -> QuerySet[CustomerPost]: ...

    @abstractmethod
    def create(self, post: Post, keywords: QuerySet[Keyword]) -> CustomerPost: ...


@dataclass
class CustomerPostService(BaseCustomerPostService):

    def create(self, post: Post, keywords: list[Keyword]) -> CustomerPost:
        customer_post = CustomerPost(customer=self.customer, post=post)
        customer_post.save()
        customer_post.keywords.add(*keywords)
        return customer_post

    def get(self, obj_id: int) -> CustomerPost:
        try:
            return self.customer.matched_posts.get(id=obj_id)
        except ObjectDoesNotExist:
            logger.error(f"Keyword with id {obj_id} not found for customer {self.customer.id}")
            raise

    def get_all(self, **filter_by) -> QuerySet[CustomerPost]:
        return (
            self.customer.matched_posts.all()
            .filter(**filter_by)
            .select_related("post")
            .prefetch_related("keywords", "post__images")
        )
