from apps.customers.services.customers import CustomerService
from apps.customers.services.oauth import CustomerLoginService


def login(username: str, password: str, telegram_id: int):
    login_service = CustomerLoginService(CustomerService())
    login_service.login(username, password, telegram_id)
