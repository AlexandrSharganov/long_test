from django.core.mail import send_mail
from django.core.cache import cache

from celery import shared_task

from long import settings

from .models import CustomUser
from .utils import generate_otp_code

@shared_task
def send_otp_to_user_email(user_id):
    """Ставим задачу на отправку письма с одноразовым кодом."""
    user = CustomUser.objects.get(id=user_id)
    otp_code = cache.get(
        key=user,
    )
    subject = 'OTP code'
    message = f'OTP code: {otp_code}'
    from_email = None 
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)