from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import BlogForm
from .models import Blog, Like
from django.views.decorators.csrf import csrf_exempt
import json



@login_required
def view_blog(request, id, slug):
    if request.method == "GET":
        blog = Blog.objects.get(id=id, slug=slug)
        liked = False

        try:
            Like.objects.get(user=request.user, blog=blog)
            liked=True
        except:
            pass

        return render(request, 'view_blog.html', {'blog': blog, "author": blog.author, "liked": liked})



@login_required
def like(request):
    if request.method == "POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            blog=request.POST.get("blog",None)

            blog = Blog.objects.get(id=blog)
            try:
                like = Like.objects.get(user=request.user, blog=blog)
                like.delete()
                liked = False
            except:
                like = Like(user = request.user, blog = blog)
                like.save()
                liked = True

            ctx = {'liked': liked}
            return HttpResponse(json.dumps(ctx))


@login_required
def new_blog(request):

    if request.method == "POST":
        blog = BlogForm(data = request.POST)

        if blog.is_valid():
            new_blog = blog.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'blog.html')

