import logging
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from apps.common.models import Blacklist, Group, Keyword
from apps.customers.models import Customer

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BaseCustomerCommonService(ABC, Generic[T]):
    def __init__(self, customer: Customer):
        self.customer = customer

    @abstractmethod
    def get(self, obj_id: int) -> T: ...

    @abstractmethod
    def get_all(self, **filter_by) -> QuerySet[T]: ...

    def activate_all(self):
        logger.info(f"Activating all {self.__class__.__name__} for customer {self.customer.id}")
        self.get_all().update(active=True)

    def activate_all_by_ids(self, ids: List[int]):
        logger.info(f"Activating {self.__class__.__name__} with IDs {ids} for customer {self.customer.id}")
        self.get_all().filter(id__in=ids).update(active=True)

    def deactivate_all(self):
        logger.info(f"Deactivating all {self.__class__.__name__} for customer {self.customer.id}")
        self.get_all().update(active=False)

    def deactivate_all_by_ids(self, ids: List[int]):
        logger.info(f"Deactivating {self.__class__.__name__} with IDs {ids} for customer {self.customer.id}")
        self.get_all().filter(id__in=ids).update(active=False)

    def get_all_active(self) -> QuerySet[T]:
        return self.get_all(is_active=True)


class CustomerGroupService(BaseCustomerCommonService[Group]):

    def get(self, obj_id: int) -> Group:
        try:
            return self.customer.groups.filter(id=obj_id).first()
        except ObjectDoesNotExist:
            logger.error(f"Group with id {obj_id} not found for customer {self.customer.id}")
            raise

    def get_all(self, **filter_by) -> QuerySet[Group]:
        return self.customer.groups.filter(**filter_by)


class CustomerKeywordService(BaseCustomerCommonService[Keyword]):

    def get(self, obj_id: int) -> Keyword:
        try:
            return self.customer.keywords.filter(id=obj_id).first()
        except ObjectDoesNotExist:
            logger.error(f"Keyword with id {obj_id} not found for customer {self.customer.id}")
            raise

    def get_all(self, **filter_by) -> List[Keyword]:
        return self.customer.keywords.filter(**filter_by)


class CustomerBlacklistService(BaseCustomerCommonService[Blacklist]):

    def get(self, obj_id: int) -> Blacklist:
        try:
            return self.customer.black_lists.get(id=obj_id)
        except ObjectDoesNotExist:
            logger.error(f"Blacklist item with id {obj_id} not found for customer {self.customer.id}")
            raise

    def get_all(self, **filter_by) -> List[Blacklist]:
        return self.customer.black_lists.filter(**filter_by)
