from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from base.email import send_email_token_otp_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
import random
from django.conf import settings

from django.core.mail import send_mail
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

# Create your models here.

class Genders(BaseModel):
    gender_name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.gender_name

class Client(BaseModel):
    profile_picture = models.ImageField(upload_to='client_picture', null=True, blank=True)
    user = models.OneToOneField(User, related_name='client_profile', on_delete=models.CASCADE)
    gender = models.ForeignKey(Genders, related_name='gender', on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=False)
    is_verified = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.user.first_name
        
class Author(BaseModel):
    profile_picture = models.ImageField(upload_to='author_picture', null=True, blank=True)
    user = models.OneToOneField(User, related_name='author_profile', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    field = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.user.first_name
    
    def first_name(self):
        return self.user.first_name




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "http://127.0.0.1:8000{}confirm/?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        "Password Reset for {title}".format(title="requested user."),
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
    )

