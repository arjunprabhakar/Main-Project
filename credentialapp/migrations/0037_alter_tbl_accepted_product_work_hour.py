# Generated by Django 3.2.18 on 2023-05-16 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0036_tbl_servicebill_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_accepted_product',
            name='work_hour',
            field=models.IntegerField(default=30, null=True),
        ),
    ]