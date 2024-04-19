from django.db import models

from apps.common.models import TimedBaseModel


class Category(TimedBaseModel):
    name = models.CharField(max_length=50, verbose_name="Category Name")

    def __str__(self):
        return self.name
