from rest_framework import serializers


def validate_video_link(value):
    """Функция-валидатор, проверяющая валидность ссылки на видео"""

    if "youtube.com" not in value:
        raise serializers.ValidationError("Можно использовать только ссылки на youtube.com")
    return value
