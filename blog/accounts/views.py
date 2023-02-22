from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

# Create your views here.

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