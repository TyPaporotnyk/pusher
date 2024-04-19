from django.db import models

from apps.common.models import TimedBaseModel
from apps.customers.models.categories import Category


class Keyword(TimedBaseModel):
    name = models.CharField(max_length=50, verbose_name="Keyword name")
    category = models.ForeignKey(Category, verbose_name="Keyword category", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.category}"
