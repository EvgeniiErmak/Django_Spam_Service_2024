# blog/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    author = models.CharField(max_length=100, verbose_name='Автор', default='Аноним')

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
