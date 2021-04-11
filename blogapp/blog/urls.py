from django.urls import path, include
from .views import new_blog, view_blog, like


urlpatterns = [
    path('new_blog/', new_blog, name='new_blog'),
    path('<int:id>/<slug:slug>', view_blog, name='view_blog'),
    path('like/', like, name='like')
]
