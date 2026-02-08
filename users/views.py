from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ["paid_course", "paid_lesson", "payment_option"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]
