# Generated by Django 4.2.7 on 2023-11-27 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_person_is_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='role',
        ),
    ]
