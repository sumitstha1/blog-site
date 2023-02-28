from django.urls import path
from .views import *
from knox.views import *

urlpatterns = [
    path('api/v1/admin', SuperUserCreationAPIView.as_view()),
    path('api/v1/users', UserAPIView.as_view()),
    path('api/v1/profile', LoggedInUser.as_view()),
    path('api/v1/users/<id>', UserAPIViewByID.as_view()),
    path('api/v1/authors/', AuthorAPIView.as_view()),
    path('api/v1/authors/<pk>', AuthorAPIViewByID.as_view()),
    path('api/v1/login', LoginAPI.as_view(), name="login"),
    path('api/v1/logout', LogoutView.as_view(), name="logout"),
    path('api/v1/logoutall', LogoutAllView.as_view(), name="logoutall"),
    path('api/v1/change_password', ChangePasswordView.as_view(), name="logoutall"),

    path('login/', client_login, name='client_login'),
    path('register/', client_register, name='client_register'),
    path('logout/', logout_page, name='logout'),
    path('author-register/', register_author, name='register_author')
]