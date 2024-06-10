from django.contrib.auth.models import BaseUserManager


class CustomerManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("You must have a nickname")
        if not email:
            raise ValueError("You must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
