from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.core.cache import cache

from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name')


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class CustomTokenObtainSerializer(serializers.Serializer):
    """Сериализатор получения токена."""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    otp_code = serializers.CharField()
    
    def validate(self, data):
        """Валидация кода подтверждения при получении токена."""
        user = get_object_or_404(CustomUser, email=data['email'])
        cached_otp = cache.get(
            key=user,
        )
        if (data['otp_code'] == cached_otp
            and check_password(data['password'], user.password)
        ):
            return data
        raise serializers.ValidationError("Your otp_code is wrong")


class GetOtpCodeSerializer(serializers.Serializer):
    """Сериализатор данных для создания OTP."""
    
    email = serializers.EmailField()
    password = serializers.CharField()
        
    def validate(self, data):
        """Валидация кода подтверждения при получении OTP."""
        user = get_object_or_404(CustomUser, email = data['email'])   
        if CustomUser.objects.filter(
            email = data['email'],
        ).exists() and check_password(data['password'], user.password):
            return data
        raise serializers.ValidationError("Your email or password is wrong")
