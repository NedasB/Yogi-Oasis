# Generated by Django 5.0.3 on 2024-04-02 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_userprofile_default_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_full_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
