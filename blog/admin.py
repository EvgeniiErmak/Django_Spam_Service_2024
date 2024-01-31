# blog/admin.py
from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'views')
    search_fields = ('title', 'content')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
