from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        verbose_name='Имя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Почта пользователя",
        help_text="Введите электронную почту",
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона пользователя",
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар пользователя",
        null=True,
        blank=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город проживания",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
