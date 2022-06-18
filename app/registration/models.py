from __future__ import unicode_literals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Username', max_length=255, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateField(_('date joined'), auto_now_add=True)
    last_login = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    user_code = models.CharField(max_length=10, null=True)
    max_left = models.PositiveIntegerField(default=10)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = "registration_user"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
