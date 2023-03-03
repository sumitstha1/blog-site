from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
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
from rest_framework.permissions import *
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer



# API View

# API for getting superuser and creating super user
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


# API for getting all the users and creating new users
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


# API for getting authors and creating authors
class AuthorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)
        context = {
            "status_code": 200,
            "message": "Authors",
            "Data": serializer.data,
            "error": []
        }
        if not author:
            return Response({"error": "No authors found."}, status=status.HTTP_204_NO_CONTENT)
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
                'is_staff': True,
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


# API for getting author with uid and updating and deleting
class AuthorAPIViewByID(APIView):
    permission_classes = [AdminPermission]
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

    def delete(self, request, pk):
        author_instance = self.get_object(pk)
        if not author_instance:
            return Response({"errors", "author not found"}, status=status.HTTP_404_NOT_FOUND)
        author_instance.delete()
        return Response({"message": "Author delete successfully"}, status=status.HTTP_200_OK)


# API for getting user with id and updating and deleting
class UserAPIViewByID(APIView):
    permission_classes = [AdminPermission]
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



# API View for generating authorization token for login
class LoginAPI(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = {
            'username': request.data.get('email'),
            'password': request.data.get('password')
        }
        serializer = AuthTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



# API Views for changing the user password
class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        if request.data.get('new_password') != request.data.get('confirm_password'):
            return Response({"new_password": ["Didn't matched."]}, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'old_password': request.data.get('old_password'),
            'new_password': request.data.get('new_password'),
        }
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            logout()

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# API View for fetching the logged in user data
class LoggedInUser(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset = None):
        user = self.request.user
        return user
    
    def get(self, request):
        self.user_obj = self.get_object()
        serializer = UserSerializer(self.user_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)








# Django views
def author_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        author_user = User.objects.filter(username = email)

        if not author_user.exists():
            messages.warning(request, 'Sorry! Your account is not registered yet.')
            return HttpResponseRedirect(request.path_info)

        if not author_user[0].author_profile.is_email_verified:
            messages.warning(request, 'Sorry! Your account is not verified yet.')
            return HttpResponseRedirect(request.path_info)

        author_user = authenticate(username = email, password = password)
        if author_user:
            login(request, author_user)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')

def client_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        client_user = User.objects.filter(username = email)

        if not client_user.exists():
            messages.warning(request, 'Sorry! Your account is not registered yet.')
            return HttpResponseRedirect(request.path_info)

        if not client_user[0].client_profile.is_verified:
            messages.warning(request, 'Sorry! Your account is not verified yet.')
            return HttpResponseRedirect(request.path_info)

        client_user = authenticate(username = email, password = password)
        if client_user:
            login(request, client_user)
            return redirect('/')

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')


def client_register(request):
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
    
def logout_page(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')
    return render(request, 'accounts/logout.html')