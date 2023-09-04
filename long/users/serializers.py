from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name')


class RegistrationSerializer(serializers.ModelSerializer):

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
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    otp_code = serializers.CharField(read_only=True)
    
    def validate(self, data):
        """
        Check that start is before finish.
        """       
        user = get_object_or_404(CustomUser, email=data['email'])
        if self.initial_data['otp_code'] != user.otp_code:
            raise serializers.ValidationError("Your otp_code is wrong")
        return data
