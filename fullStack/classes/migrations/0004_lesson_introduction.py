# Generated by Django 5.0.3 on 2024-04-09 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_alter_lesson_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='introduction',
            field=models.TextField(blank=True, null=True),
        ),
    ]
