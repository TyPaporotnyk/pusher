from django.db import models

from apps.common.models import TimedBaseModel
from apps.customers.models.categories import Category


class Group(TimedBaseModel):
    name = models.CharField(max_length=50, verbose_name="Group Name")
    url = models.URLField(verbose_name="Group URL")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Group Category")

    def __str__(self):
        return f"{self.name} - {self.category}"
