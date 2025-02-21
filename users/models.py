from django.db import models
from django.contrib.auth.models import AbstractUser
from education.models import Course, Lesson


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        verbose_name='Имя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Почта пользователя",
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="Номер телефона",
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


class Payments(models.Model):
    PAYMENT_STATUS = [
        ("cash", "наличные"),
        ("transfer", "перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name="Пользователь"
    )
    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата оплаты"
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course',
        verbose_name="Оплаченный курс",
        null=True, blank=True
    )
    separately_paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='lesson',
        verbose_name="Оплаченный урок",
        null=True,
        blank=True
    )
    payment_amount = models.IntegerField(
        default=0,
        verbose_name="Сумма оплаты",
        null=True,
        blank=True
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default="cash",
        verbose_name="Способ оплаты",
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.user} {self.paid_course}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
