from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/admin', SuperUserCreationAPIView.as_view()),
    path('api/v1/users', UserAPIView.as_view()),
    path('api/v1/users/<id>', UserAPIViewByID.as_view()),
    path('api/v1/authors/', AuthorAPIView.as_view()),
    path('api/v1/authors/<pk>', AuthorAPIViewByID.as_view()),
    path('api/v1/login', LoginView.as_view()),

    path('', login, name='login'),
    path('register/', register, name='register'),
    path('author-register/', register_author, name='register_author')
]