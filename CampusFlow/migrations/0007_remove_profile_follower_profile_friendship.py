# Generated by Django 5.1.1 on 2024-09-26 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CampusFlow', '0006_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='follower',
        ),
        migrations.AddField(
            model_name='profile',
            name='friendship',
            field=models.ManyToManyField(blank=True, to='CampusFlow.profile'),
        ),
    ]
