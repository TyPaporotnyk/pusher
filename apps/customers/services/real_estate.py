from abc import ABC, abstractmethod

from apps.customers.models.real_estate import RealEstate


class BaseRealEstateService(ABC):

    @staticmethod
    @abstractmethod
    def get_or_create(real_estate_id: int, website: str) -> RealEstate:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_last_id_by_tag(website: str) -> RealEstate:
        raise NotImplementedError


class RealEstateService(BaseRealEstateService):

    @staticmethod
    def get_last_id_by_tag(website: str) -> int:
        instance = RealEstate.objects.filter(website=website).order_by("-real_estate_id").first()
        return instance.real_estate_id if instance else 0

    @staticmethod
    def get_or_create(real_estate_id: int, website: str) -> RealEstate:
        real_estate, _ = RealEstate.objects.get_or_create(real_estate_id=real_estate_id, website=website)
        return real_estate
