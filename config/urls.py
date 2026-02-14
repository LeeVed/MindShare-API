from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # админка
    path("admin/", admin.site.urls),
    # JWT аутентификация
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Приложения
    path("courses/", include("courses.urls")),
    path("users/", include("users.urls", namespace="users")),
]
