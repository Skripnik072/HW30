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
    city = models.CharField(
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


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Плательщик",
        help_text="Укажите плательщика",
    )
    date = models.DateField(
        verbose_name="Дата платежа", help_text="Введите дату платежа"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма платежа",
        help_text="Введите сумму платежа",
    )
    payment_method = models.CharField(
        max_length=50,
        verbose_name="Метод платежа",
        choices=[('cash', 'наличные'), ('transfer', 'перевод')],
    )
    paid_course = models.ForeignKey(
        'materials.Course',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплачен курс",
    )
    paid_lesson = models.ForeignKey(
        'materials.Lesson',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплачен урок",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        help_text="Укажите подписчика",
    )

    course = models.ForeignKey(
        'materials.Course',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Подписка на курс",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"