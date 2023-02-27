from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import generics
from base.rest_permission import *


# Create your views here.

# API Views

class CategoryApiView(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializers(category, many=True)
        context = {
            "status_code": 200,
            "message": "Article Category",
            "Data": serializer.data,
            "error": []
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        data = {
                'category_name': request.data.get('category')
            }
        serializer = CategorySerializers(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryApiViewById(APIView):
    def get_object(self, uid):
        try:
            return Category.objects.get(uid = uid)
        except:
            return None

    def delete(self, request, uid):
        user_instance = self.get_object(uid)
        if not user_instance:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        user_instance.delete()
        return Response({"message": "Delete Successfully"}, status=status.HTTP_200_OK)

    def get(self, request, uid):
        category_instance = self.get_object(uid)
        if not category_instance:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializers(category_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostApiView(APIView):
    def get(self, request):
        article = Articles.objects.all()
        serializer = ArticleSerializers(article, many=True)
        context = {
            "status_code": 200,
            "message": "Articles",
            "Data": serializer.data,
            "error": []
        }
        return Response(context, status=status.HTTP_200_OK)


class ApprovePost(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminPermission]
    serializer_class = ArticleSerializers
    queryset = Articles.objects.all()

















# Web View

def article(request, slug):
    article = Articles.objects.get(slug = slug)
    category = Category.objects.all()
    context = {
        'article_detail': article,
        'categories': category,

    }
    return render(request, 'articles/article_detail.html', context)