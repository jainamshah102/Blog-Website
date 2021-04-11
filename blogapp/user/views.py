from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import UserForm
from blog.models import Blog, Like, Comment


def index(request):

    if request.method == "GET":
        blogs = Blog.objects.filter(status=1)
        likes_comments = []
        for blog in blogs:
            likes = Like.objects.filter(blog = blog).count()
            comments = Comment.objects.filter(blog = blog).count()
            likes_comments.append({"likes": likes, "comments": comments})
        print(likes_comments)
        return render(request, 'index.html', {"blogs_data": zip(blogs, likes_comments)})

def register(request):

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            return HttpResponseRedirect(reverse('login'))
   
        return render(request, 'registration.html', {'form': user_form})

    return render(request, 'registration.html')



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


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



