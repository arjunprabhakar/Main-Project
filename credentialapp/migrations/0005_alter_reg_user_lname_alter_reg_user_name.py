# Generated by Django 4.1.2 on 2022-11-04 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0004_alter_reg_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reg_user',
            name='lname',
            field=models.CharField(max_length=200, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='reg_user',
            name='name',
            field=models.CharField(max_length=200, verbose_name='First Name'),
        ),
    ]
