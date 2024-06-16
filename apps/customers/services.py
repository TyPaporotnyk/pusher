from abc import ABC, abstractmethod
from typing import Any

from django.db.models import QuerySet

from apps.common.models import Blacklist, Category, Group, Keyword
from apps.customers.models import Customer
from apps.posts.models import Post


class BaseCustomerService(ABC):
    def __init__(
        self,
        *,
        request: Any | None = None,
        obj: Customer | None = None,
    ):
        if obj is None:
            self.customer = request.user
        else:
            self.customer = obj

    @staticmethod
    @abstractmethod
    def get_all_customers() -> QuerySet[Customer]: ...

    @abstractmethod
    def get_customer(self) -> Customer: ...

    @abstractmethod
    def get_customer_groups(self, active: bool | None = None) -> QuerySet[Group]: ...

    @abstractmethod
    def get_customer_keywords(self, active: bool | None = None) -> QuerySet[Keyword]: ...

    @abstractmethod
    def get_customer_category(self) -> QuerySet[Category]: ...

    @abstractmethod
    def get_customer_black_list(self, active: bool | None = None) -> QuerySet[Blacklist]: ...

    @abstractmethod
    def get_customer_matched_posts(self, ordering: str) -> QuerySet[Post]: ...

    @abstractmethod
    def deactivate_customer_keywords(self): ...
    @abstractmethod
    def deactivate_customer_groups(self): ...

    @abstractmethod
    def activate_customer_keywords(self, keyword_ids: list[int]): ...
    @abstractmethod
    def activate_customer_groups(self, group_ids: list[int]): ...


class CustomerService(BaseCustomerService):

    @staticmethod
    def get_all_customers() -> QuerySet[Customer]:
        return Customer.objects.all()

    def get_customer_matched_posts(self, ordering: str) -> QuerySet[Post]:
        return (
            self.customer.matched_posts.all()
            .order_by(ordering)
            .select_related("post")
            .prefetch_related("keywords", "post__images")
        )

    def get_customer(self) -> Customer:
        return self.customer

    def get_customer_category(self) -> QuerySet[Category]:
        return self.customer.categories.all()

    def get_customer_groups(self, active: bool | None = None) -> QuerySet[Group]:
        if active is None:
            return self.customer.groups.all()
        else:
            return self.customer.groups.all().filter(is_active=active)

    def get_customer_keywords(self, active: bool | None = None) -> QuerySet[Keyword]:
        if active is None:
            return self.customer.keywords.all()
        else:
            return self.customer.keywords.all().filter(is_active=active)

    def get_customer_black_list(self, active: bool | None = None) -> QuerySet[Blacklist]:
        if active is None:
            return self.customer.black_lists.all()
        else:
            return self.customer.black_lists.all().filter(is_active=active)

    def deactivate_customer_keywords(self):
        customer_keywords = self.get_customer_keywords().filter(is_active=True)
        customer_keywords.update(is_active=False)

    def deactivate_customer_groups(self):
        customer_groups = self.get_customer_groups().filter(is_active=True)
        customer_groups.update(is_active=False)

    def activate_customer_keywords(self, keyword_ids: list[int]):
        self.get_customer_keywords().filter(id__in=keyword_ids).update(is_active=True)

    def activate_customer_groups(self, group_ids: list[int]):
        self.get_customer_groups().filter(id__in=group_ids).update(is_active=True)
