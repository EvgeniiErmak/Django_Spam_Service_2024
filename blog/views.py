# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-publication_date']  # Сортировка по дате публикации
    paginate_by = 10  # Пагинация (по умолчанию 10 постов на странице)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'