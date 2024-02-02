# mailing_service/models.py
from django.db import models
from django.utils import timezone


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, unique=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.email


class Mailing(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    clients = models.ManyToManyField(Client)
    start_time = models.DateTimeField(default=timezone.now)  # По умолчанию - текущее время
    end_time = models.DateTimeField(blank=True, null=True)   # Поле может быть пустым
    frequency = models.CharField(choices=FREQUENCY_CHOICES, default='daily', max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')  # По умолчанию - создана

    def __str__(self):
        return self.title

    def set_created_status(self):
        self.status = 'created'
        self.save()

    def set_started_status(self):
        self.status = 'started'
        self.save()

    def set_completed_status(self):
        self.status = 'completed'
        self.save()

    def activate_mailing(self):
        self.start_time = timezone.now()
        self.set_started_status()

    def complete_mailing(self):
        self.end_time = timezone.now()
        self.set_completed_status()


class Message(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    subject = models.CharField(max_length=355)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Log(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(default=timezone.now)  # По умолчанию - текущее время
    status = models.CharField(max_length=50)
    response = models.TextField(blank=True)

    def __str__(self):
        return f"{self.attempt_time} - {self.status}"
