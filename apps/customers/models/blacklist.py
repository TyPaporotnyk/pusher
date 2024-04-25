from django.db import models

from apps.customers.models.categories import Category


class Blacklist(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, null=True, blank=True, verbose_name="Black list category", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} - {self.category}"
