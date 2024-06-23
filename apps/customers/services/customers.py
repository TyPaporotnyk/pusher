from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.customers.models import Customer
from apps.customers.services.common import (
    BaseCustomerCommonService,
    CustomerBlacklistService,
    CustomerGroupService,
    CustomerKeywordService,
)
from apps.customers.services.posts import BaseCustomerPostService, CustomerPostService


@dataclass(kw_only=True)
class BaseCustomerService(ABC):
    customer: Customer
    _keyword_service: Optional[BaseCustomerCommonService] = field(default=None, init=False)
    _group_service: Optional[BaseCustomerCommonService] = field(default=None, init=False)
    _blacklist_service: Optional[BaseCustomerCommonService] = field(default=None, init=False)
    _posts_service: Optional[BaseCustomerPostService] = field(default=None, init=False)

    @property
    def keyword_service(self) -> BaseCustomerCommonService:
        if not self._keyword_service:
            self._keyword_service = CustomerKeywordService(self.customer)
        return self._keyword_service

    @property
    def group_service(self) -> BaseCustomerCommonService:
        if not self._group_service:
            self._group_service = CustomerGroupService(self.customer)
        return self._group_service

    @property
    def black_list_service(self) -> BaseCustomerCommonService:
        if not self._blacklist_service:
            self._blacklist_service = CustomerBlacklistService(self.customer)
        return self._blacklist_service

    @property
    def posts_service(self) -> BaseCustomerPostService:
        if not self._posts_service:
            self._posts_service = CustomerPostService(self.customer)
        return self._posts_service


class CustomerService(BaseCustomerService):

    @staticmethod
    def get_all() -> QuerySet[Customer]:
        return Customer.objects.all()

    @staticmethod
    def get(obj_id: int) -> Customer:
        return get_object_or_404(Customer, pk=obj_id)
