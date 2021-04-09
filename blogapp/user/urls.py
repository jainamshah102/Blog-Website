from django.urls import path, include
from .views import login_user, index


urlpatterns = [
    path('index/', index, name='index'),
    path('login/', login_user, name='login')
]

