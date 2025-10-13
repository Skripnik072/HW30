from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="установите аватар",
    )
    cyti = models.CharField(
        max_length=20,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="введите город",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
