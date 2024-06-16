from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from apps.base.pagination import Pagination
from apps.common.serializers import BlacklistSerializer, GroupSerializer, KeywordSerializer
from apps.customers.serializers import CustomerPostSerializer, CustomerSerializer
from apps.customers.services import CustomerService


@extend_schema(tags=["Customer"])
class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer()

    def get_object(self):
        return self.get_queryset()


@extend_schema(tags=["Customer"])
class UpdateCustomerView(generics.UpdateAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer()

    def get_object(self):
        return self.get_queryset()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        groups_ids = request.data.get("groups", [])
        keyword_ids = request.data.get("keywords", [])

        customer_service = CustomerService(request=self.request)

        # Groups
        customer_service.deactivate_customer_groups()
        customer_service.activate_customer_groups(groups_ids)

        # Keywords
        customer_service.deactivate_customer_keywords()
        customer_service.activate_customer_keywords(keyword_ids)

        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(tags=["Customer"])
class CustomerGroupView(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer_groups()

    def perform_create(self, serializer):
        customer = CustomerService(request=self.request).get_customer()
        serializer.save(customer=customer)


@extend_schema(tags=["Customer"])
class CustomerKeywordView(viewsets.ModelViewSet):
    serializer_class = KeywordSerializer

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer_keywords()

    def perform_create(self, serializer):
        customer = CustomerService(request=self.request).get_customer()
        serializer.save(customer=customer)


@extend_schema(tags=["Customer"])
class CustomerBlackListView(viewsets.ModelViewSet):
    serializer_class = BlacklistSerializer

    def get_queryset(self):
        return CustomerService(request=self.request).get_customer_black_list()

    def perform_create(self, serializer):
        customer = CustomerService(request=self.request).get_customer()
        serializer.save(customer=customer)


@extend_schema(tags=["Customer"])
class CustomerPostView(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomerPostSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        last_post_id = self.request.query_params.get("last_post_id", None)
        ordering = self.request.query_params.get("ordering", "-created_at")

        posts = CustomerService(request=self.request).get_customer_matched_posts(ordering=ordering)

        if last_post_id is not None:
            if "-" in ordering:
                posts = posts.filter(id__lt=last_post_id)
            else:
                posts = posts.filter(id__gt=last_post_id)

        return posts
