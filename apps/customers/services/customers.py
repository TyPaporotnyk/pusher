from abc import ABC, abstractmethod

from apps.customers.models.customers import Customer


class BaseCustomerService(ABC):
    @staticmethod
    @abstractmethod
    def get(username: str, password: str) -> Customer:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_all_by_group(group: str) -> list[Customer]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_all_by_keyword(keyword: str) -> list[Customer]:
        raise NotImplementedError


class CustomerService(BaseCustomerService):

    @staticmethod
    def get_all_by_group(group: str) -> list[Customer]:
        return Customer.objects.filter(is_active=True).filter(groups__name=group).all()

    @staticmethod
    def get_all_by_keyword(keyword: str) -> list[Customer]:
        return Customer.objects.filter(is_active=True).filter(keywords__name=keyword).all()

    @staticmethod
    def get(username: str, password: str) -> Customer:
        return Customer.objects.filter(username=username, password=password).first()
