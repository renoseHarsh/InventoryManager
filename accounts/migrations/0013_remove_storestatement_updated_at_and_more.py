# Generated by Django 4.2.7 on 2023-11-30 10:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_storestatement_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storestatement',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='storestatement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
