from django.contrib import admin
from .models import Post, Category, Comment
from django.contrib.auth.models import Permission

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'last_modified', 'previous_post', 'next_post')
    save_on_top = True
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_created', 'last_modified')
    save_on_top = True
    list_filter = ['date_created']
    search_fields = ['title']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'post', 'created_on')
    save_on_top = True
    list_filter = ('created_on',)
    search_fields = ('user', 'content')

admin.site.site_header = 'Admin Panel'
admin.site.index_title = 'Blog Site Administration'
admin.site.site_title = 'Django Blog'
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Permission)