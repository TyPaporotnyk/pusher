from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db.models import QuerySet

from apps.customers.models import Customer
from apps.customers.repository import CustomerRepository


@dataclass(frozen=True)
class BaseCustomerService(ABC):
    customer_repository: CustomerRepository

    @abstractmethod
    def get_customer_by_id(self, customer_id: str) -> Customer: ...

    @abstractmethod
    def get_active_customers(self) -> QuerySet[Customer]: ...


@dataclass(frozen=True)
class CustomerService(BaseCustomerService):

    def get_customer_by_id(self, customer_id: str) -> Customer:
        return self.customer_repository.get(pk=customer_id)

    def get_active_customers(self) -> QuerySet[Customer]:
        return self.customer_repository.get_all().filter(is_active=True)
