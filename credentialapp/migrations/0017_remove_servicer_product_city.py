# Generated by Django 4.1.2 on 2023-02-28 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0016_servicer_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicer_product',
            name='city',
        ),
    ]
