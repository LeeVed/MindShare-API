from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "description_short", "lesson_count")
    list_filter = ("name",)
    search_fields = ("name", "description")

    def description_short(self, obj):
        return obj.description[:50] + "..." if obj.description else ""

    description_short.short_description = "Описание"

    def lesson_count(self, obj):
        return obj.lessons.count()

    lesson_count.short_description = "Кол-во уроков"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "video_link", "has_preview")
    list_filter = ("course",)
    search_fields = ("name", "description", "video_link")

    def has_preview(self, obj):
        return bool(obj.preview)

    has_preview.boolean = True
    has_preview.short_description = "Есть превью"
