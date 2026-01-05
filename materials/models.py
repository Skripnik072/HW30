from django.db import models
from django.conf import settings


class Course(models.Model):
    """Описание модели Курс"""

    name = models.CharField(
        max_length=100,
        verbose_name="Курс",
        help_text="Введите название курса",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )

    preview = models.ImageField(
        upload_to="materials/media",
        blank=True,
        null=True,
        verbose_name="фото",
        help_text="Загрузите картинку",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец курса",
        blank=True,
        null=True,
        help_text="Укажите владельца курса",
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
        verbose_name="Время последнего обновления",)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Описание модели Урок"""

    name = models.CharField(
        max_length=50, verbose_name="Урок", help_text="Введите название урока"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="описание урока",
        help_text="Введите описание урока",
    )

    picture = models.ImageField(
        upload_to="materials/media",
        blank=True,
        null=True,
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
        help_text="Введите название курса",
        related_name='lessons',
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец урока",
        blank=True,
        null=True,
        help_text="Укажите владельца урока",
    )

    video = models.FileField(
        upload_to="materials/media",
        blank=True,
        null=True,
        help_text="Загрузите видео",
    )

    url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Ссылка", help_text="Загрузите ссылку",)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
