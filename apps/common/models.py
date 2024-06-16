from django.db import models

from apps.base.models import TimedBaseModel
from apps.customers.models import Customer


class Category(TimedBaseModel):
    name = models.CharField(max_length=255, verbose_name="Category Name")
    customer = models.ForeignKey(
        Customer, verbose_name="Customer", on_delete=models.CASCADE, related_name="categories"
    )

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

    def __str__(self):
        return self.name


class Group(TimedBaseModel):
    url = models.URLField(unique=True, verbose_name="Group URL")
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Group Category"
    )
    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE, related_name="groups")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.name:
            return f"{self.name} - {self.category}"
        else:
            return f"{self.url} - {self.category}"


class Keyword(TimedBaseModel):
    name = models.TextField(verbose_name="Keyword name")
    category = models.ForeignKey(
        Category, null=True, blank=True, verbose_name="Keyword category", on_delete=models.CASCADE
    )
    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE, related_name="keywords")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
