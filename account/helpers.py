import uuid
from django.core.mail import send_mail
from django.conf import settings

def generate_token():
    token = str(uuid.uuid4())
    return token

def send_registration_token_mail(username, email, token):
    subject = "Verify user account."
    message = f'Hi {username}!, click the link to verify your account http://127.0.0.1:8000/verify/{token}/'
    recipient_list = [email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list )

def send_forgetPassword_token_mail(email, token):
    subject = 'Your forget password link.'
    message = f'Hi! click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False,)
    return True