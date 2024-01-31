# blog/views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import Post, Comment
from .forms import CommentForm
from django.urls import reverse


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-publication_date']
    paginate_by = 10


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_object(self):
        obj = super().get_object()
        obj.views += 1  # Увеличиваем количество просмотров при каждом просмотре поста
        obj.save()
        return obj

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts, 'form': CommentForm()})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    post.views += 1
    post.save()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': post.comments.all()})
