# Generated by Django 3.2.18 on 2023-05-16 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0034_user_address_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_servicebill',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]