from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import BlogForm
from .models import Blog, Like
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
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

            blog = Blog.objects.get(id = blog)
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


@login_required
def view_drafts(request):

    if request.method == "GET":
        blogs = Blog.objects.filter(author = request.user, status=0)

        return render(request, 'drafts.html', {'blogs': blogs})

    return render(request, 'drafts.html')


@login_required
def view_published(request):

    if request.method == "GET":
        blogs = Blog.objects.filter(author = request.user, status = 1)

        return render(request, 'published.html', {'blogs': blogs})

    return render(request, 'published.html')


@login_required
def publish_blog(request, blog):
    blog = Blog.objects.get(id = blog)

    if blog.author == request.user:
        if request.method == "GET":

            if blog.author == request.user:
                blog.publish()
                return redirect('view_blog', id=blog.id, slug=blog.slug)

        return render(request, 'drafts.html')

    else:
        raise Http404


@login_required
def delete_blog(request, blog, published=0):
    blog = Blog.objects.get(id = blog)

    if blog.author == request.user:

        if request.method == "GET":
            blog.delete()

        if published:
            return HttpResponseRedirect(reverse('view_published'))
        else:
            return HttpResponseRedirect(reverse('view_drafts'))
    else:
        raise Http404


@login_required
def edit_blog(request, blog, slug):
    blog = Blog.objects.get(id = blog, slug = slug)

    if blog.author == request.user:

        if request.method == 'POST':
            edited_blog = BlogForm(request.POST, instance=blog)

            if edited_blog.is_valid():
                edited_blog.save()

                if blog.status == 0:
                    return redirect('view_draft_blog', id=blog.id, slug=blog.slug)
                else:
                    return redirect('view_blog', id=blog.id, slug=blog.slug)

        return render(request, 'edit_blog.html', {'blog': blog})

    else:
        raise Http404


@login_required
def view_draft_blog(request, blog, slug):
    blog = Blog.objects.get(id = blog, slug = slug)

    if blog.author == request.user:
        return render(request, 'view_draft_blog.html', {'blog': blog})

    else:
        raise Http404
