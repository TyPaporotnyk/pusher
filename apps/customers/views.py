from rest_framework import viewsets

from apps.customers.permissions import IsAdmin
from apps.customers.repository import CustomerRepository
from apps.customers.serializers import CustomerSerializer
from apps.customers.services import CustomerService


class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        customer_repository = CustomerRepository()
        customer_service = CustomerService(customer_repository=customer_repository)
        return customer_service.get_active_customers()


class CustomerOwnerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()
