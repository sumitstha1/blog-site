from django.urls import path
from .views import *

urlpatterns = [

    # API Urls
    path('api/v1/posts', PostApiView.as_view()),
    path('api/v1/post_approval/<pk>', ApprovePost.as_view()),
    path('api/v1/category', CategoryApiView.as_view()),
    path('api/v1/category/<uid>', CategoryApiViewById.as_view()),






    # Web Urls

    path('<slug>', article, name="product_detail")
]