# Generated by Django 4.2.7 on 2023-11-30 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_storestatement_itemquantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storestatement',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
