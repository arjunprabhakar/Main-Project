# Generated by Django 3.2.18 on 2023-05-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0033_tbl_accepted_product_work_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_address',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
