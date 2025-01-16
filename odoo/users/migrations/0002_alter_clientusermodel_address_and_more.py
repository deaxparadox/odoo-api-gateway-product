# Generated by Django 5.1.5 on 2025-01-16 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientusermodel',
            name='address',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Shipping/billing address'),
        ),
        migrations.AlterField(
            model_name='clientusermodel',
            name='phone',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Phone number'),
        ),
    ]
