from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Минимальный менеджер для работы с email вместо username"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # Полностью удаляем поле username

    email = models.EmailField(verbose_name="почта", unique=True)
    phone_number = models.CharField(verbose_name="номер телефона", max_length=15, blank=True, null=True)
    city = models.CharField(verbose_name="город", max_length=50, blank=True, null=True)
    avatar = models.ImageField(verbose_name="аватар", upload_to='users/avatars/', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Поля для createsuperuser

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель платежей"""

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_OPTIONS = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
        related_name="payments"
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты",
        help_text="Дата и время платежа"
    )
    paid_course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        help_text="Выберите оплаченный курс",
        related_name="payments"
    )
    paid_lesson = models.ForeignKey(
        "courses.Lesson",     # приложение и модель
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        help_text="Выберите оплаченный урок",
        related_name="payments"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
        help_text="Введите сумму оплаты"
    )
    payment_option = models.CharField(
        max_length=20,
        choices=PAYMENT_OPTIONS,
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

        constraints = [
            models.CheckConstraint(
                condition=(
                        models.Q(paid_course__isnull=False, paid_lesson__isnull=True) |
                        models.Q(paid_course__isnull=True, paid_lesson__isnull=False)
                ),
                name="only_course_or_lesson"
            )
        ]

    def __str__(self):
        if self.paid_course:
            return f"{self.user.email} - {self.paid_course.name} - {self.amount} руб."
        elif self.paid_lesson:
            return f"{self.user.email} - {self.paid_lesson.name} - {self.amount} руб."
        else:
            return f"{self.user.email} - {self.amount} руб." # защита от непредвиденной ситуации(промежуточное состояние)
