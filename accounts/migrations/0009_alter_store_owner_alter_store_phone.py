# Generated by Django 4.2.7 on 2023-11-29 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='owner',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
