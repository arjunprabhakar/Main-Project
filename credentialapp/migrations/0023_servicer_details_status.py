# Generated by Django 4.1.2 on 2023-03-11 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0022_servicer_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicer_details',
            name='status',
            field=models.BooleanField(default=0),
        ),
    ]
