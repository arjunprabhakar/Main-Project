# Generated by Django 4.1.2 on 2022-10-27 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product_qty',
            field=models.IntegerField(default=1),
        ),
    ]
