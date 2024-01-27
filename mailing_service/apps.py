# mailing_service/apps.py
from django.apps import AppConfig


class MailingServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_service'

    def ready(self):
        # Вызывается при загрузке приложения
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from .tasks import EmailTask

        scheduler = BackgroundScheduler()
        scheduler.start()

        scheduler.add_job(
            EmailTask.send_emails,
            trigger=CronTrigger(second="*/10"),
            id="send_emails_job",
            replace_existing=True,
        )

        from django_apscheduler.jobstores import DjangoJobStore

        # Проверяем, нет ли уже job store с алиасом "default"
        if "default" not in scheduler.jobstores:
            scheduler.add_jobstore(DjangoJobStore(), "default")
