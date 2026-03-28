from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Course, Lesson, Subscription
from courses.validators import validate_video_link


class LessonSerializer(ModelSerializer):
    video_link = serializers.URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, course):
        """Подсчитывает количество уроков в курсе"""

        return course.lessons.count()

    def get_is_subscribed(self, course):
        """Проверяет, подписан ли текущий пользователь на курс"""

        user = self.context.get(
            "request"
        ).user  # какой пользователь сделал запрос к API
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=course).exists()
        return False
