# Generated by Django 5.2 on 2025-04-29 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='company',
        ),
        migrations.RemoveField(
            model_name='card',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='card',
            name='order',
        ),
    ]
