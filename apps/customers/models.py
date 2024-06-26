from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.base.models import TimedBaseModel
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


class CustomerPost(TimedBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="matched_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="matched_users")
    keywords = models.ManyToManyField("common.Keyword", blank=True, related_name="posts_keywords")
