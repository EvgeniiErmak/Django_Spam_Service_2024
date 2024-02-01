# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-publication_date']  # Сортировка по дате публикации
    paginate_by = 4  # Пагинация (по умолчанию 4 постов на странице)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
