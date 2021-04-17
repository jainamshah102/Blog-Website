from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm, UpdateForm
from blog.models import Blog, Like, Comment
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from .models import User, Follow
from notifications.signals import notify
from django.db.models import Count
import json


def index(request):

    if request.method == "GET":
        top_blogs = Blog.objects.filter(status=1).order_by('-published_on')
        top_blogs = sorted(top_blogs, key=lambda b: b.likes()
                           * b.comments(), reverse=True)[:6]

        likes_comments = []

        for blog in top_blogs:
            likes_comments.append(
                {"likes": blog.likes(), "comments": blog.comments()})

        top_authors = User.objects.all()
        top_authors = sorted(
            top_authors, key=lambda a: a.followers(), reverse=True)[:10]

        author_followers = []

        for author in top_authors:
            author_followers.append(
                {"followers": author.followers(), "publishes": author.publishes()})

        return render(request, 'index.html', {
            "blogs_data": zip(top_blogs, likes_comments),
            "top_authors": zip(top_authors, author_followers)
        })


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
            nxt = request.GET.get("next", None)

            if nxt is None:
                return HttpResponseRedirect(reverse('index'))

            elif not is_safe_url(url=nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return HttpResponseRedirect(reverse('index'))

            return redirect(nxt)

        else:
            return render(request, 'login.html', {"error": "Invalid username or password!"})

    return render(request, 'login.html', {})


def about(request):
    return render(request, 'about.html')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def view_profile(request, email=None):

    if request.method == "GET":
        if not email:
            blogs = Blog.objects.filter(author=request.user, status=1)
            return render(request, 'view_profile.html', {"user": request.user, 'blogs': blogs, "current_user": request.user})
        else:
            user = User.objects.get(email=email)
            blogs = Blog.objects.filter(author=user,  status=1)
            return render(request, 'view_profile.html', {'user': user, 'blogs': blogs, "current_user": request.user})

    return render(request, 'view_profile.html')


@login_required
def edit_profile(request):

    if request.method == "POST":
        user = UpdateForm(request.POST, request.FILES, instance=request.user)

        if user.is_valid():
            user.save()
            return HttpResponseRedirect(reverse('view_profile'))

        return render(request, 'edit_profile.html', {'user': request.user})

    return render(request, 'edit_profile.html')


@login_required
def follow(request):

    if request.method == "POST" and request.POST.get('operation') == "follow" and request.is_ajax():
        author = request.POST.get("author", None)
        if author != request.user.id:
            author = User.objects.get(id=author)

            follows = False

            try:
                follow = Follow.objects.get(user=request.user, author=author)
                follow.delete()
                follows = False
            except:
                follow = Follow(user=request.user, author=author)
                follow.save()
                follows = True

            content = {"follows": follows}

            return HttpResponse(json.dumps(content))
