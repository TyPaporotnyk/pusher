from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.common.models import Blacklist, Group, Keyword
from apps.customers.managers import CustomerManager
from apps.posts.models import Post


class Customer(AbstractBaseUser):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    max_pack = models.PositiveIntegerField(default=0)
    groups = models.ManyToManyField(Group, blank=True)
    groups_keywords = models.ManyToManyField(Keyword, blank=True, related_name="groups_keywords")
    keywords = models.ManyToManyField(Keyword, blank=True, related_name="keywords")
    blacklist = models.ManyToManyField(Blacklist, blank=True, related_name="blacklist")

    matched_posts = models.ManyToManyField(Post, blank=True, related_name="matched_posts")
    telegram_id = models.BigIntegerField(blank=True, null=True)

    objects = CustomerManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self) -> str:
        return self.username

    @property
    def match_post_count(self):
        return self.matched_posts.count()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
