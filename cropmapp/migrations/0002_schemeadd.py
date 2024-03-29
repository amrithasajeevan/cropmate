# Generated by Django 5.0.1 on 2024-02-06 06:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropmapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchemeAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme_name', models.CharField(blank=True, max_length=100, null=True)),
                ('start_age', models.IntegerField(null=True)),
                ('end_age', models.IntegerField(null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('link', models.CharField(blank=True, max_length=1000, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
