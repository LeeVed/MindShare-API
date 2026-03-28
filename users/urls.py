from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CustomUserViewSet, PaymentViewSet, StripePaymentView

app_name = "users"

router = SimpleRouter()
router.register(r"payments", PaymentViewSet)
router.register(r"users", CustomUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # регистрация пользователя
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # создание оплаты
    path("create-payment/", StripePaymentView.as_view(), name="create-payment"),
]
