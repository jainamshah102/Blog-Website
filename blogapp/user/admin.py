from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Follow


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',
                    'date_joined', 'gender', 'about', 'name')
    list_filter = ('email', 'is_staff', 'is_active', 'gender', 'name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'date_joined', 'gender', 'avatar', 'about', 'name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'date_joined', 'gender', 'avatar', 'about', 'name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'timestamp',)
    list_filter = ('user', 'author',)
    search_fields = ['user', 'author']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
