from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel
from apps.user.manager import UserManager


class User(AbstractBaseUser, BaseModel):
    username = None
    phone_number = models.CharField(max_length=13, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=250)
    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        return self.full_name or self.phone_number
