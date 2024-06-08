from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from apps.customers.managers import AccountManager


class Customer(AbstractBaseUser):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
