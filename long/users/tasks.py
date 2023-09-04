from django.core.mail import send_mail

from celery import shared_task

from .models import CustomUser
from .utils import generate_otp_code

@shared_task
def send_otp_to_user_email(user_id):
    """Ставим задачу на отправку письма с одноразовым кодом."""
    user = CustomUser.objects.get(id=user_id)
    otp_code = generate_otp_code()
    user.otp_code = otp_code
    user.save()
    
    subject = 'Ваш OTP код'
    message = f'Ваш OTP код: {otp_code}'
    from_email = 'noreply@example.com'  # Замените на ваш адрес электронной почты
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)