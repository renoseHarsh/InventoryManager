# Generated by Django 5.0 on 2023-12-10 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_person_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='last_name',
        ),
        migrations.AddField(
            model_name='person',
            name='full_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
