from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Payment
from .serializers import CustomUserSerializer, PaymentSerializer
from .services import create_payment_session


class PaymentViewSet(viewsets.ModelViewSet):
    """Класс представление для реализации CRUD для платежей"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["paid_course", "paid_lesson", "payment_option"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Класс представление для реализации CRUD для пользователей,
    в т.ч. регистрации пользователей
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":  # только регистрация
            return [AllowAny()]
        return [IsAuthenticated()]  # все остальные CRUD


class StripePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        lesson_id = request.data.get("lesson_id")
        amount = request.data.get("amount")

        if not course_id and not lesson_id:
            return Response(
                {"error": "Укажите course_id или lesson_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.create(
            user=request.user,
            paid_course_id=course_id,
            paid_lesson_id=lesson_id,
            amount=amount,
            payment_option="stripe",
        )

        success_url = "https://example.com/success"
        cancel_url = "https://example.com/cancel"

        checkout_url = create_payment_session(payment, success_url, cancel_url)

        return Response(
            {
                "checkout_url": checkout_url,
                "payment_id": payment.id,
                "message": "Перейдите по ссылке для оплаты",
            }
        )
