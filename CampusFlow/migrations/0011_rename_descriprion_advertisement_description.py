# Generated by Django 5.1.1 on 2024-10-03 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CampusFlow', '0010_alter_profile_profile_picture_alter_profile_usn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='descriprion',
            new_name='description',
        ),
    ]