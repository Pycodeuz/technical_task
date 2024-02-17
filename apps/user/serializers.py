import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.user.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """admin user create serializer"""

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'password']

    def validate_phone_number(self, value):  # Validator is to validate how correctly phone_number is
        if not value:
            raise serializers.ValidationError("Telefon raqamni kiritishingiz majburiy!")
        if not re.match(r'^\d{12}$', value):
            raise serializers.ValidationError("Telefon raqam noto'g'ri formatda.")
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Ushbu telefon raqam allaqachon ro'yxatdan o'tgan.")
        return value

    def validate(self, attrs):
        user = User(
            full_name=attrs['full_name'],
            phone_number=attrs['phone_number'],
            password=make_password(attrs['password'])
        )
        user.save()
        return super().validate(attrs)


class UserGetMeSerializer(serializers.ModelSerializer):
    """Get User me serializer"""

    class Meta:
        model = User
        fields = ["id", "phone_number", 'full_name']
