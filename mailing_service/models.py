# mailing_service/models.py
from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True)  # Уникальность почты
    full_name = models.CharField(max_length=100, unique=True)  # Уникальность имени
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.email


class Mailing(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    clients = models.ManyToManyField(Client)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    delivery_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')])

    def __str__(self):
        return self.title


class Message(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    subject = models.CharField(max_length=355)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Log(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    response = models.TextField(blank=True)

    def __str__(self):
        return f"{self.attempt_time} - {self.status}"