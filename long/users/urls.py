from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import register, user_profile, other_profile, profile_list, delete_account, CustomObtainAuthToken


app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='custom_obtain_token'),
    path('profile/me/', user_profile, name='profile'),
    path('profile/', profile_list, name='profile_list'),
    path('profile/<int:pk>/', other_profile, name='other_profile'),
    path('delete/', delete_account, name='delete_account'),
]