from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import register, user_profile, delete_account, CustomObtainAuthToken


app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='custom_obtain_token'),
    path('profile/', user_profile, name='profile'),
    path('delete/', delete_account, name='delete_account'),
]