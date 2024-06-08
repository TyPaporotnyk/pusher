from rest_framework import viewsets

from apps.customers.serializers import CustomerSerializer


class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()
