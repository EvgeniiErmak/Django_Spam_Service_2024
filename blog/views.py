# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post
from django.shortcuts import get_object_or_404


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-publication_date']  # Сортировка по дате публикации
    paginate_by = 4  # Пагинация (по умолчанию 4 постов на странице)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        # Получаем объект статьи
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        # Увеличиваем счетчик просмотров
        post.views += 1
        post.save()

        return super().get(request, *args, **kwargs)
