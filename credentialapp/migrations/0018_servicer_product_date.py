# Generated by Django 4.1.2 on 2023-02-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0017_remove_servicer_product_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicer_product',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]