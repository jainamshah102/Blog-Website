from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import BlogForm

@login_required
def new_blog(request):

    if request.method == "POST":
        blog = BlogForm(data = request.POST)

        if blog.is_valid():
            new_blog = blog.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            return HttpResponseRedirect(reverse('login'))

    return render(request, 'blog.html')
