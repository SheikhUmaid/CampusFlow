# Generated by Django 5.1.1 on 2024-10-03 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CampusFlow', '0011_rename_descriprion_advertisement_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='event_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]