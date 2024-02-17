import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.school.models import School
from apps.school.serializers import SchoolSerializer
from apps.users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """This serializer is used to create new admin or user"""

    class Meta:
        model = User
        fields = [
            'full_name',
            'role',
            'phone_number',
            'password',
            'image'
        ]

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
            password=make_password(attrs['password']),
            role=attrs['role'],
            is_active=True,
            image=attrs['image']
        )
        user.save()
        return super().validate(attrs)


class UserRetriveSerializer(serializers.ModelSerializer):
    schools = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            'full_name',
            "role",
            "upd_status",
            "image",
            "schools"
        ]

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def get_schools(self, obj):
        try:
            schools_qs = obj.school_set.all()
            schools_data = SchoolSerializer(schools_qs, many=True).data
            return schools_data
        except School.DoesNotExist:
            return None


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone_number',
            'full_name',
            'password',
            "image"
        ]
