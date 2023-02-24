from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/posts', PostApiView.as_view()),
    path('api/v1/post_approval/<pk>', ApprovePost.as_view()),
    path('api/v1/category', CategoryApiView.as_view()),
    path('api/v1/category/<uid>', CategoryApiViewById.as_view()),
]