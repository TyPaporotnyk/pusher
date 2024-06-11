from django.db import models

from apps.base.models import TimedBaseModel


class Category(TimedBaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Category Name")

    def __str__(self):
        return self.name


class Blacklist(TimedBaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, null=True, blank=True, verbose_name="Black list category", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} - {self.category}"


class Group(TimedBaseModel):
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Group Name")
    url = models.URLField(unique=True, verbose_name="Group URL")
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Group Category"
    )

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

    def __str__(self):
        return f"{self.name} - {self.category}"
