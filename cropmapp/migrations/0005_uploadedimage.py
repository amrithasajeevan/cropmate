# Generated by Django 5.0.2 on 2024-02-22 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropmapp', '0004_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
            ],
        ),
    ]
