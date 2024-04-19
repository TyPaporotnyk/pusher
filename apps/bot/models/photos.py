from django.db import models

from apps.common.models import TimedBaseModel


class Photo(TimedBaseModel):
    photo_url = models.URLField(unique=True, verbose_name="Photo URL")
    photo_id = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Photo ID")

    def __str__(self):
        return self.photo_url
