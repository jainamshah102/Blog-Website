from django.contrib import admin
from .models import Blog, Like, Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on', )
    list_filter = ('title', 'status', 'created_on', 'updated_on', )
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog','timestamp',)
    list_filter = ('user', 'blog','timestamp',)
    search_fields = ['user', 'blog']    


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog','comment','timestamp')
    list_filter = ('user', 'blog','timestamp')
    search_fields = ['user', 'blog']

    
admin.site.register(Blog, BlogAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
