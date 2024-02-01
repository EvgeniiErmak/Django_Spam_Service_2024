# blog/models.py
from django.utils import timezone
from django.db import models
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(upload_to='media/images/', null=True, blank=True, verbose_name='Изображение')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            # Проверяем, было ли изображение изменено
            try:
                this = Post.objects.get(id=self.id)
                if this.image != self.image:
                    self.image.delete(save=False)  # Удаляем старое изображение
            except: pass

            # Масштабируем изображение
            img = Image.open(self.image)
            output_size = (500, 500)  # Установите желаемый размер
            img.thumbnail(output_size)
            img.save(self.image.path)

        super().save(*args, **kwargs)
