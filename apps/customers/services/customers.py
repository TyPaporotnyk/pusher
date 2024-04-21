from abc import ABC, abstractmethod

from apps.customers.models.customers import Customer


class BaseCustomerService(ABC):
    @staticmethod
    @abstractmethod
    def get(**kwargs) -> Customer:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_all_by_group_url(group_url: str) -> list[Customer]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_all_by_keyword(keyword: str) -> list[Customer]:
        raise NotImplementedError


class CustomerService(BaseCustomerService):

    @staticmethod
    def get_all_by_group_url(group_url: str) -> list[Customer]:
        return Customer.objects.filter(is_active=True).filter(groups__url=group_url).all()

    @staticmethod
    def get_all_by_keyword(keyword: str) -> list[Customer]:
        return Customer.objects.filter(is_active=True).filter(keywords__name=keyword).all()

    @staticmethod
    def get(**kwargs) -> Customer:
        return Customer.objects.filter(**kwargs).first()
