# Generated by Django 4.2.5 on 2024-02-27 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cropmapp', '0009_farmerproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='razorpay_order_id',
        ),
    ]