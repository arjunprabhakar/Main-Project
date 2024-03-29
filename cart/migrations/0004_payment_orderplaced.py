# Generated by Django 4.1.2 on 2022-11-20 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0002_tbl_review'),
        ('credentialapp', '0009_log_user_status_alter_log_user_otp'),
        ('cart', '0003_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(blank=True, null=True)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razorpay_payment_status', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='credentialapp.user_address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credentialapp.log_user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=10)),
                ('is_ordered', models.BooleanField(default=False)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='credentialapp.user_address')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productapp.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='credentialapp.log_user')),
            ],
        ),
    ]
