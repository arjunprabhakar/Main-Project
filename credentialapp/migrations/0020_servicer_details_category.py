# Generated by Django 4.1.2 on 2023-03-11 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('credentialapp', '0019_alter_log_user_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicer_details',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='category.category'),
        ),
    ]