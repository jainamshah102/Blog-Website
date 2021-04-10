from django.urls import path, include
from .views import new_blog

urlpatterns = [
    path('new_blog/', new_blog, name='new_blog')
]
