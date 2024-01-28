# mailing_service/tasks.py
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Mailing, Message, Log
from django.utils import timezone

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


class EmailTask:
    @classmethod
    def start(cls):
        cls.scheduler = BackgroundScheduler()
        cls.scheduler.add_jobstore(DjangoJobStore(), "default")
        cls.scheduler.start()

        # Реализация запуска периодических задач
        cls.scheduler.add_job(cls.send_emails, 'cron', hour='*/3', timezone='Europe/Moscow')  # Каждые 3 часа по Московскому времени

    @classmethod
    def send_emails(cls):
        # Получение всех рассылок, которые нужно отправить сейчас
        current_time = timezone.now()
        mailings = Mailing.objects.filter(start_time__lte=current_time, end_time__gte=current_time)

        for mailing in mailings:
            # Отправка сообщений для каждой рассылки
            for client in mailing.clients.all():
                # Отправка сообщения
                message = Message.objects.create(mailing=mailing, subject=mailing.title, body=mailing.content)
                # Логирование попытки отправки
                Log.objects.create(message=message, attempt_time=current_time, status='Отправка запущена')

                # Здесь должен быть код для отправки сообщения клиенту, но он опущен в этом примере

                # Обновление статуса попытки отправки в логах
                Log.objects.filter(pk=message.log_set.last().pk).update(status='Сообщение отправлено успешно')

        # Реализация отправки писем

    @classmethod
    def stop(cls):
        # Реализация остановки задачи
        cls.scheduler.shutdown()
