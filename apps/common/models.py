from django.db import models

from apps.base.models import TimedBaseModel
from apps.customers.models import Customer


class Category(TimedBaseModel):
    name = models.CharField(max_length=255, verbose_name="Category Name")

    def __str__(self):
        return self.name


class Blacklist(TimedBaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, null=True, blank=True, verbose_name="Black list category", on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer, verbose_name="Customer", on_delete=models.CASCADE, related_name="black_lists"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "customer"], name="unique_black_list_name_customer")]

    def __str__(self):
        return self.name


class Group(TimedBaseModel):
    url = models.URLField(verbose_name="Group URL")
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Group Category"
    )
    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE, related_name="groups")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["url", "customer"], name="unique_url_customer")]

    def __str__(self):
        return f"{self.url} - {self.category}"


class Keyword(TimedBaseModel):
    name = models.CharField(max_length=255, verbose_name="Keyword name")
    category = models.ForeignKey(
        Category, null=True, blank=True, verbose_name="Keyword category", on_delete=models.CASCADE
    )
    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE, related_name="keywords")
    is_active = models.BooleanField(default=True)

    @property
    def posts_count(self) -> int:
        return self.posts_keywords.count()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "customer"], name="unique_name_customer")]

    def __str__(self):
        return self.name


class PublicGroup(TimedBaseModel):
    url = models.URLField(verbose_name="Group URL")

    def __str__(self):
        return self.url


class PublicKeyword(TimedBaseModel):
    name = models.CharField(max_length=255, verbose_name="Public Keyword Name")

    def __str__(self):
        return self.name


class PublicBlackList(TimedBaseModel):
    name = models.CharField(max_length=255, verbose_name="Public Keyword Name")

    def __str__(self):
        return self.name
