from .models import Supplier
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class GeneralMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)
    detail = serializers.CharField(max_length=500)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20)
    firstname = serializers.CharField(max_length=100, required=True)
    lastname = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, allow_blank=True, trim_whitespace=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=100, allow_blank=True, trim_whitespace=True, required=True, validators=[validate_password])


class LoginResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=500)


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=100, allow_blank=False, trim_whitespace=True, required=True, validators=[validate_password])


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            "password", "is_active", 'user_permissions', 'groups', 'is_staff', "is_superuser", "last_login"
        ]


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = [
            "id", "name", "phone", "address"
        ]
