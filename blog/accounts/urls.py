from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='login'),
    path('register/', register, name='register'),
    path('author-register/', register_author, name='register_author')
]