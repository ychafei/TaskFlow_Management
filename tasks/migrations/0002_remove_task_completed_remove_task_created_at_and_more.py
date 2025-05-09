# Generated by Django 5.1.6 on 2025-02-19 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='task',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('not_completed', 'Not Completed'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='not_completed', max_length=20),
        ),
    ]
