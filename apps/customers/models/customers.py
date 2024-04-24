from django.db import models

from apps.common.models import TimedBaseModel
from apps.customers.models.groups import Group
from apps.customers.models.keywords import Keyword
from apps.customers.models.real_estate import RealEstate


class Customer(TimedBaseModel):
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    password = models.CharField(max_length=120)
    max_pack = models.IntegerField(default=0)
    registration_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    real_estates = models.ManyToManyField(RealEstate, blank=True)
    telegram_id = models.BigIntegerField(blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True)
    groups_keywords = models.ManyToManyField(Keyword, blank=True, related_name="groups_keywords")
    keywords = models.ManyToManyField(Keyword, blank=True, related_name="keywords")

    def is_advert_contains(self, advert: RealEstate) -> bool:
        return advert in self.real_estates.all()

    def add_advert(self, advert: RealEstate):
        self.real_estates.add(advert)
        self.save()

    @property
    def posts_received(self):
        return len(self.real_estates.all())

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
