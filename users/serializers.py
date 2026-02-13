from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Payment, CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class CustomUserSerializer(ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password", "phone_number", "city", "avatar"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],  # ← create_user хэширует пароль
            phone_number=validated_data.get("phone_number", ""),
            city=validated_data.get("city", ""),
            avatar=validated_data.get("avatar", None)
        )
        return user
