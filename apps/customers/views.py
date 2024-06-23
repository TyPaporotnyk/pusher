from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from apps.base.pagination import Pagination
from apps.common.serializers import BlacklistSerializer, GroupSerializer, KeywordSerializer
from apps.customers.filters import CustomerPostFilter
from apps.customers.serializers import CustomerPostSerializer, CustomerSerializer, CustomerTelegramSerializer
from apps.customers.services.customers import CustomerService


@extend_schema(tags=["Customer"])
class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return CustomerService(customer=self.request.user).customer

    def get_object(self):
        return self.get_queryset()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        customer_service = CustomerService(customer=self.request.user)

        if (groups_ids := request.data.get("groups")) is not None:
            customer_service.group_service.deactivate_all()
            customer_service.group_service.activate_all_by_ids(groups_ids)

        if (keyword_ids := request.data.get("keywords")) is not None:
            customer_service.keyword_service.deactivate_all()
            customer_service.keyword_service.activate_all_by_ids(keyword_ids)

        if (black_lists_ids := request.data.get("black_lists")) is not None:
            customer_service.black_list_service.deactivate_all()
            customer_service.black_list_service.activate_all_by_ids(black_lists_ids)

        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(tags=["Customer"])
class CustomerGroupView(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return CustomerService(customer=self.request.user).group_service.get_all()

    def perform_create(self, serializer):
        customer = CustomerService(customer=self.request.user).customer
        serializer.save(customer=customer)


@extend_schema(tags=["Customer"])
class CustomerKeywordView(viewsets.ModelViewSet):
    serializer_class = KeywordSerializer

    def get_queryset(self):
        return CustomerService(customer=self.request.user).keyword_service.get_all()


@extend_schema(tags=["Customer"])
class CustomerBlackListView(viewsets.ModelViewSet):
    serializer_class = BlacklistSerializer

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer_black_list()

    def perform_create(self, serializer):
        customer = CustomerService(request=self.request).get_customer()
        serializer.save(customer=customer)


@extend_schema(tags=["Customer"])
class CustomerPostView(viewsets.ModelViewSet):
    serializer_class = CustomerPostSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_at"]
    filterset_class = CustomerPostFilter
    ordering = ["-created_at"]

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer_matched_posts()


@extend_schema(tags=["Customer"])
class CustomerTelegramView(viewsets.ModelViewSet):
    serializer_class = CustomerTelegramSerializer

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer()

    def get_object(self):
        return self.get_queryset()
