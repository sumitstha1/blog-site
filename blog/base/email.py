from django.core.mail import send_mail
from django.conf import settings

def send_email_token_otp_mail(email, email_token):
    subject = "Your account needs to be verified!!!"
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, this if blogging site. In order to validate your account you need to verify your account clicking the link below:\n http://127.0.0.1:8000/accounts/activate/{email_token}'

    send_mail(subject, message, email_from, [email])