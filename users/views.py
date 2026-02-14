from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment, CustomUser
from .serializers import PaymentSerializer, CustomUserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Класс представление для реализации CRUD для платежей"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["paid_course", "paid_lesson", "payment_option"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]


class CustomUserViewSet(viewsets.ModelViewSet):
    """Класс представление для реализации CRUD для пользователей, в т.ч. регистрации пользователей"""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":  # только регистрация
            return [AllowAny()]
        return [IsAuthenticated()]   # все остальные CRUD
