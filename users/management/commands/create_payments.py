from decimal import Decimal

from django.core.management.base import BaseCommand

from courses.models import Course, Lesson
from users.models import CustomUser, Payment


class Command(BaseCommand):
    help = "Создает тестовые платежи для модели Payment"

    def handle(self, *args, **options):

        user, created = CustomUser.objects.get_or_create(
            email="test@example.com",
            defaults={
                "phone_number": "+79991234567",
                "city": "Москва",
            },
        )
        if created:
            user.set_password("testpass123")
            user.save()
            self.stdout.write(f"Создан тестовый пользователь: {user.email}")

        try:
            course = Course.objects.first()
            lesson = Lesson.objects.first()

            if not course or not lesson:
                self.stdout.write(self.style.ERROR("Сначала создайте курсы и уроки!"))
                return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при получении курса/урока: {e}")
            )
            return

        payments_data = [
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": None,
                "amount": Decimal("15000.00"),
                "payment_option": "transfer",
            },
            {
                "user": user,
                "paid_course": None,
                "paid_lesson": lesson,
                "amount": Decimal("3000.00"),
                "payment_option": "cash",
            },
            {
                "user": user,
                "paid_course": course,
                "paid_lesson": None,
                "amount": Decimal("12000.0"),
                "payment_option": "transfer",
            },
            {
                "user": user,
                "paid_course": None,
                "paid_lesson": lesson,
                "amount": Decimal("2500.00"),
                "payment_option": "cash",
            },
        ]

        created_count = 0
        for data in payments_data:
            payment, created = Payment.objects.get_or_create(
                user=data["user"],
                paid_course=data["paid_course"],
                paid_lesson=data["paid_lesson"],
                amount=data["amount"],
                payment_option=data["payment_option"],
            )
            if created:
                created_count += 1
                self.stdout.write(f"Создан платеж: {payment}")
            else:
                self.stdout.write(f"Платеж уже существует: {payment}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано {created_count} платежей из {len(payments_data)}"
            )
        )
