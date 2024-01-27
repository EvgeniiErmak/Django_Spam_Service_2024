# Generated by Django 5.0.1 on 2024-01-27 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('full_name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')], max_length=20)),
                ('clients', models.ManyToManyField(to='mailing_service.client')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=355)),
                ('body', models.TextField()),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing_service.mailing')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField()),
                ('status', models.CharField(max_length=50)),
                ('response', models.TextField(blank=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing_service.message')),
            ],
        ),
    ]
