# Generated by Django 4.1.2 on 2023-03-27 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0008_alter_productgallery_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sentiment_score',
            field=models.FloatField(default=0),
        ),
    ]
