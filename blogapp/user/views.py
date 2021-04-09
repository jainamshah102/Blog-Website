from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse



def index(request):

    if request.method == "GET":
        return render(request, 'index.html', {})



def login_user(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        
        else:
            return render(request, 'login.html', {"error": "Invalid username or password!"})
    
    return render(request, 'login.html', {})
