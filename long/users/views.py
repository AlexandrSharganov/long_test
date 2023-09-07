from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .tasks import send_otp_to_user_email
from .models import CustomUser
from .serializers import UserSerializer, RegistrationSerializer, CustomTokenObtainSerializer, GetOtpCodeSerializer
from .permissions import IsAdminOrOwner
from .utils import generate_otp_code


@api_view(['POST'])
@permission_classes([])
def get_otp_code(request):
    """Функция получения одноразового кода."""
    if request.method == 'POST':
        serializer = GetOtpCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(CustomUser, email=serializer.validated_data['email'])
            otp_code = generate_otp_code()
            cache.set(
                key=user,
                value=otp_code,
                timeout=60 * 2
            )
            send_otp_to_user_email.delay(user.id)
            return Response(
                {'message': f'otp verification code have been sended to {user.email}'},
                status=status.HTTP_200_OK
            )
    


class CustomObtainAuthToken(ObtainAuthToken):
    """Кастомная вьюха для получения токена."""
    
    serializer_class = CustomTokenObtainSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(CustomUser, email=serializer.validated_data['email'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([])
def register(request):
    """Функция регистрации."""
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(email=request.data['email'])
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Функция получения или редактирования информации своего профиля."""
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def other_profile(request, pk=None):
    """Функция получения информации чужого профиля."""
    if request.method == 'GET':
        if pk:
            serializer = UserSerializer(get_object_or_404(CustomUser, id=pk))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_list(request):
    """Функция получения списка профилей."""
    serializer = UserSerializer(CustomUser.objects.all(), many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminOrOwner])
def delete_account(request):
    """Функция удаления профиля."""
    request.user.delete()
    return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)