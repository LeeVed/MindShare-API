from django.db import models

from config import settings


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название курса",
        help_text="Введите название курса",
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
        help_text="Напишите о курсе",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Владелец",
        related_name="courses",
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
        help_text="Введите название урока",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание урока", help_text="Опишите урок"
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
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lessons",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Владелец",
        related_name="lessons",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "name"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Модель подписки на обновления курса для пользователя"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscriptions",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")  # защита от дублей
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} подписан на {self.course}"
