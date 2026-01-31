from django.db import models


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название курса",
        help_text="Введите название курса"
    )
    preview = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Напишите о курсе"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название урока",
        help_text="Введите название урока"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Опишите урок"
    )
    preview = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для урока",
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Введите ссылку на видео урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lessons",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "name"]

    def __str__(self):
        return self.name
