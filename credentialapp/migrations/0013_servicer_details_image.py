# Generated by Django 4.1.2 on 2023-02-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentialapp', '0012_servicer_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicer_details',
            name='image',
            field=models.ImageField(blank=True, upload_to='Service'),
        ),
    ]