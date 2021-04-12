from django.urls import path, include
from .views import new_blog, view_blog, like, view_drafts, view_published, publish_blog, delete_blog


urlpatterns = [
    path('new_blog/', new_blog, name='new_blog'),
    path('<int:id>/<slug:slug>', view_blog, name='view_blog'),
    path('like/', like, name='like'),
    path('drafts/', view_drafts, name='view_drafts'),
    path('published/', view_published, name='view_published'),
    path('publish_blog/<int:blog>', publish_blog, name='publish_blog'),
    path('delete_blog/<int:blog>/<int:published>', delete_blog, name='delete_blog'),
]
