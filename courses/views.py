from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Course, Lesson, Subscription
from .paginators import CoursePaginator, LessonPaginator
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import generics
from users.permissions import IsSuperUser, IsOwner, IsModerator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .tasks import send_course_update_email


class CourseViewSet(ModelViewSet):
    """Представление для списка курсов
      (промотр всего списка, промотр 1 курса, создание курса,
       редакция курса, удаление курса
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]
        if self.action == "retrieve":
            permission = IsModerator | IsOwner
            return [IsAuthenticated(), permission()]
        if self.action == "create":
            permission = ~IsModerator | IsSuperUser
            return [IsAuthenticated(), permission()]
        if self.action in ["update", "partial_update"]:
            permission = IsModerator | IsOwner | IsSuperUser
            return [IsAuthenticated(), permission()]
        if self.action == "destroy":
            permission = IsOwner | IsSuperUser
            return [IsAuthenticated(), permission()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.save()
        send_course_update_email.delay(course.id)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Представление для списка всех уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        elif self.request.method == "POST":
            permission = ~IsModerator | IsSuperUser
            return [IsAuthenticated(), permission()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для каждого урока
      (просмотр,редакция и удаление урока)
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission = IsModerator | IsOwner | IsSuperUser
            return [IsAuthenticated(), permission()]
        elif self.request.method in ["PUT", "PATCH"]:
            permission = IsModerator | IsOwner | IsSuperUser
            return [IsAuthenticated(), permission()]
        elif self.request.method == "DELETE":
            permission = IsOwner | IsSuperUser
            return [IsAuthenticated(), permission()]
        return [IsAuthenticated()]


class SubscriptionAPIView(APIView):
    """Представление для создания и удаления подписки"""

    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"

        return Response({"message": message})
