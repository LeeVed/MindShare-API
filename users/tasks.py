from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def block_inactive_users():
    """
    Проверяет  пользователей по дате последнего входа по полю last_login
    и блокирует, если пользователь не заходил более месяца
    """

    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(last_login__lt=month_ago, is_active=True)
    count = inactive_users.count()
    if count > 0:
        inactive_users.update(is_active=False)
        return f"Заблокировано {count} неактивных пользователей"
    return "Нет пользователей для блокировки"
