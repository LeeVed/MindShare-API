from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PaymentViewSet

app_name = "users"

router = SimpleRouter()
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
