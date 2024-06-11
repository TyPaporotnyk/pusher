from apps.base.repository import Repository
from apps.customers.models import Customer


class CustomerRepository(Repository[Customer]):
    model = Customer
