from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets

from apps.common.models import Blacklist, Category, Group, Keyword
from apps.common.serializers import BlacklistSerializer, CategorySerializer, GroupSerializer, KeywordSerializer


@extend_schema(tags=["Common"])
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]


@extend_schema(tags=["Common"])
class GroupView(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name", "category__name"]
    search_fields = ["name", "category__name"]


@extend_schema(tags=["Common"])
class KeywordView(viewsets.ModelViewSet):
    serializer_class = KeywordSerializer
    queryset = Keyword.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name", "category__name"]
    search_fields = ["name", "category__name"]


@extend_schema(tags=["Common"])
class BlackListView(viewsets.ModelViewSet):
    serializer_class = BlacklistSerializer
    queryset = Blacklist.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["name", "category__name"]
    search_fields = ["name", "category__name"]
