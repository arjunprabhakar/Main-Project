# Generated by Django 3.2.18 on 2023-05-09 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0031_alter_tbl_accepted_product_service_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_accepted_product',
            name='service_bill',
            field=models.FileField(null=True, upload_to='Service_Bill'),
        ),
    ]
