from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создает и заполняет группу модераторов правами"

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="moderators")

        Course = apps.get_model("courses", "Course")
        Lesson = apps.get_model("courses", "Lesson")
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        group.permissions.clear()

        permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct],
            codename__in=[
                "view_course",
                "change_course",
                "view_lesson",
                "change_lesson",
            ],
        )

        group.permissions.set(permissions)
