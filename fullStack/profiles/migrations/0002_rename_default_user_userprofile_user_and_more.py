# Generated by Django 5.0.3 on 2024-04-01 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_user',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_country',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='default_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
