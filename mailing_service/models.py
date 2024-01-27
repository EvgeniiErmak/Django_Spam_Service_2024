# mailing_service/models.py
from django.db import models


class Client(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True)


class Mailing(models.Model):
    send_time = models.DateTimeField()
    frequency = models.CharField(max_length=20, choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')])
    status = models.CharField(max_length=20, choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')])


class Message(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()


class Log(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    response = models.TextField(blank=True)
