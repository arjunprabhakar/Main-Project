# Generated by Django 4.1.2 on 2023-02-27 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0011_alter_log_user_options_alter_reg_user_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicer_Details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=200, null=True, verbose_name='First Name')),
                ('lname', models.CharField(max_length=200, null=True, verbose_name='Last Name')),
                ('phone_no', models.CharField(max_length=200, null=True)),
                ('hname', models.CharField(max_length=200, null=True)),
                ('street', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('district', models.CharField(max_length=200, null=True)),
                ('pin', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credentialapp.log_user', verbose_name='Email')),
            ],
        ),
    ]
