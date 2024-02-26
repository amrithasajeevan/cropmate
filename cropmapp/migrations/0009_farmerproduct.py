# Generated by Django 4.2.5 on 2024-02-26 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cropmapp', '0008_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_type', models.CharField(choices=[('Vegetables', 'Vegetables'), ('Fruits', 'Fruits'), ('Grains', 'Grains')], default='Vegetables', max_length=200)),
                ('crop_name', models.CharField(blank=True, max_length=500, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('price', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_available', models.BooleanField(blank=True, default=True, null=True)),
                ('posted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
