from django.db import models

from apps.common.models import TimedBaseModel


class RealEstate(TimedBaseModel):
    real_estate_id = models.BigIntegerField(null=True, blank=True, verbose_name="Real Estate ID")
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name="Website")

    def __str__(self):
        return f"{self.real_estate_id}"
