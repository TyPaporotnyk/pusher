from django.db import models

from apps.common.models import TimedBaseModel
from apps.customers.models.categories import Category


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
