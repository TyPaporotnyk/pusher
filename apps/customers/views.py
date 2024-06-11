from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.customers.repository import CustomerRepository
from apps.customers.serializers import CustomerSerializer
from apps.customers.services import CustomerService


@extend_schema(tags=["Customer"])
class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        customer_repository = CustomerRepository()
        customer_service = CustomerService(customer_repository=customer_repository)
        return customer_service.get_active_customers()


@extend_schema(tags=["Customer"])
class CustomerOwnerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()
