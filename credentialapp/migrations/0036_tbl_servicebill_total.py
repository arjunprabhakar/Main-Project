# Generated by Django 3.2.18 on 2023-05-16 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0035_tbl_servicebill_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_servicebill',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]
