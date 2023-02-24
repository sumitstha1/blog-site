from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import uuid
from django.contrib import messages
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.rest_permission import AdminPermission
from rest_framework import generics

# Create your views here.
class SuperUserCreationAPIView(APIView):
    def get(self, request):
        user = User.objects.filter(is_superuser = True)
        serializer = AdminSerializer(user, many=True)
        context = {
            "status_code": 200,
            "message": "Admin Users",
            "Data": serializer.data,
            "error": []
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        password1 = request.data['password1']
        password2 = request.data['password2']
        if password1 == password2:
            data = {
                'username': request.data.get('username'),
                'email': request.data.get('email'),
                'password': password1,
                'is_staff': True,
                'is_active': True,
                'is_superuser': True
            }
            serializer = AdminSerializer(data=data)
        
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        context = {
            "status_code": 200,
            "message": "Users",
            "Data": serializer.data,
            "error": []
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorAPIView(APIView):
    def get(self, request):
        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)
        context = {
            "status_code": 200,
            "message": "Authors",
            "Data": serializer.data,
            "error": []
        }
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        email_token = str(uuid.uuid4())
        data = {
            'user': {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'username': request.data['email'],
                'email': request.data.get('email'),
                'password': request.data.get('password'),
                'is_staff': True
            },
            'bio': request.data.get('bio'),
            'field': request.data.get('field'),
            'profile_picture': request.data.get('profile_picture'),
            'email_token': email_token,
            'is_email_verified': False
        }
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorAPIViewByID(APIView):
    def get_object(self, pk):
        try:
            return Author.objects.get(pk = pk)
        except:
            return None

    def get(self, request, pk):
        author_instance = self.get_object(pk)
        if not author_instance:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(author_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        author_instance = self.get_object(pk)
        data = {
            'user': {
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name'),
                'password': request.data.get('password'),
            },
            'bio': request.data.get('bio'),
            'field': request.data.get('field'),
            'profile_picture': request.data.get('profile_picture')
        }
        data.get('user').pop('username', None)
        print(data.get('user'))
        serializer = AuthorSerializer(instance = author_instance, data = data)
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIViewByID(APIView):
    def get_object(self, id):
        try:
            return User.objects.get(id = id)
        except:
            return None

    def get(self, request, id):
        user_instance = self.get_object(id)
        if not user_instance:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user_instance = self.get_object(id)
        if not user_instance:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user_instance, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user_instance = self.get_object(id)
        if not user_instance:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        user_instance.delete()
        return Response({"message": "Delete Successfully"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'message': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login Success'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Credentials', 'email': email, 'password': password}, status=status.HTTP_401_UNAUTHORIZED)

def login(request):
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already exists')
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = password, username = email)
        user_obj.set_password(password)
        user_obj.save()
        client = Client.objects.create(user = user_obj, nickname = "Sumit")
        client.save()
        messages.success(request, 'An email has been sent on your mail.')
        return render(request, 'accounts/register.html')
    return render(request, 'accounts/register.html')
    

def register_author(request):
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        auth_email = request.POST.get('email')
        auth_password = request.POST.get('password')

        user = User.objects.filter(username = auth_email)

        if user.exists():
            messages.warning(request, 'Email is already exists')
            return HttpResponseRedirect(request.path_info)

        user = User.objects.create(first_name = fname, last_name = lname, email = auth_email, password = auth_password, username = auth_email)
        user.set_password(auth_password)
        user.is_staff = True
        user.save()
        author = Author.objects.create(user = user, bio = "Sumit")
        author.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/author_register.html')