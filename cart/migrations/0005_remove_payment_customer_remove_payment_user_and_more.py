# Generated by Django 4.1.2 on 2022-11-20 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_payment_orderplaced'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.DeleteModel(
            name='OrderPlaced',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
