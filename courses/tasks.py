from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """
    Отправляет уведомление об обновлении курса всем подписчикам
    """
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course).select_related("user")
    recipient_list = [sub.user.email for sub in subscriptions if sub.user.email]

    if not recipient_list:
        return f"Нет подписчиков у курса {course.name}"

    subject = f"Обновление курса: {course.name}"
    message = f"""
    Уважаемый пользователь!
    Курс "{course.name}" был обновлен.
    Зайдите в свой аккаунт, чтобы посмотреть новые материалы.
    Ссылка на курс: {settings.SITE_URL}/courses/{course.id}

    С уважением,
    команда проекта
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=True,
    )

    return (
        f"Уведомление отправлено {len(recipient_list)} подписчикам курса {course.name}"
    )
