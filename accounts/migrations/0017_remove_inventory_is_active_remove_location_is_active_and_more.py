# Generated by Django 5.0 on 2023-12-11 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_inventory_is_active_location_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='location',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='person',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='person',
            name='is_owner',
        ),
        migrations.RemoveField(
            model_name='store',
            name='is_active',
        ),
    ]