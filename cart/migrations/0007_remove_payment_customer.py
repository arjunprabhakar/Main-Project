# Generated by Django 4.1.2 on 2022-11-20 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='customer',
        ),
    ]