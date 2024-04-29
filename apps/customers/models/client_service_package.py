from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import TimedBaseModel


class ClientServicePackage(TimedBaseModel):
    name = models.CharField(max_length=255)
    max_groups_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_keywords_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_comments_per_month = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_facebook_profile_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    use_ai = models.BooleanField(default=False)

    def __str__(self):
        return self.name
