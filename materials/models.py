from django.db import models


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
    )

    video = models.FileField(
        upload_to="materials/media",
        blank=True,
        null=True,
        verbose_name="Видео",
        help_text="Загрузите видео",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
