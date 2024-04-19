from dataclasses import dataclass

from django.utils import timezone

from apps.customers.exceptions import CustomerIsAllReadyRegistered, CustomerIsNotRegistered
from apps.customers.models.customers import Customer
from apps.customers.services.customers import BaseCustomerService


@dataclass(frozen=True)
class CustomerLoginService:
    customer_service: BaseCustomerService

    def login(self, username: str, password: str, telegram_id: int) -> Customer:
        customer = self.customer_service.get(username=username, password=password)

        if customer is None:
            raise CustomerIsNotRegistered

        elif customer.telegram_id is not None:
            raise CustomerIsAllReadyRegistered

        customer.telegram_id = telegram_id
        customer.registration_date = timezone.now()
        customer.is_active = True
        customer.save()

        return customer
