from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    full_name = models.CharField(
        max_length=50
    )
    avatar = models.ImageField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    facebook_id = models.CharField(blank=True, null=True, max_length=100)
    about = models.CharField(
        max_length=255,
        blank=True, null=True
    )

    is_deleted = models.BooleanField(
        default=False
    )
    is_invited = models.BooleanField(
        default=False
    )
    invitation_date = models.DateTimeField(
        null=True,
        blank=True
    )
    registration_date = models.DateTimeField(
        null=True,
        blank=True
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('full_name',)
