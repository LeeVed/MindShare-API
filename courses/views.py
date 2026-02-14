from rest_framework.viewsets import ModelViewSet
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import generics
from users.permissions import IsSuperUser, IsOwner, IsModerator
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(ModelViewSet):
    """Представление для курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Представление для списка всех уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

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
    """Представление для каждого урока"""

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
