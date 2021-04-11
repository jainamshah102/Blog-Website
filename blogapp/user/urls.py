from django.urls import path, include
from .views import login_user, logout_user, register, view_profile, edit_profile


urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('view_profile/', view_profile, name='view_profile'),
    path('view_profile/<email>', view_profile, name='view_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]
