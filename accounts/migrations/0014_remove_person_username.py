# Generated by Django 5.0 on 2023-12-10 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_storestatement_updated_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='username',
        ),
    ]
