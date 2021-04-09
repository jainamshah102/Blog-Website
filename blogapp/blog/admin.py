from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on', )
    list_filter = ('title', 'status', 'created_on', 'updated_on', )
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Blog, BlogAdmin)
