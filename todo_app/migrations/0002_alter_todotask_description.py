# Generated by Django 5.1.4 on 2024-12-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todotask',
            name='description',
            field=models.TextField(help_text='Detailed description of the task'),
        ),
    ]