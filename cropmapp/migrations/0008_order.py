# Generated by Django 4.2.5 on 2024-02-23 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cropmapp', '0007_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=1000, null=True)),
                ('equipment_names', models.TextField(blank=True, null=True)),
                ('quantities', models.TextField(blank=True, null=True)),
                ('prices', models.TextField(blank=True, null=True)),
                ('total', models.FloatField()),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('estimated_date', models.DateField(blank=True, null=True)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('order-placed', 'order-placed'), ('cancelled', 'cancelled')], default='order-placed', max_length=200)),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]