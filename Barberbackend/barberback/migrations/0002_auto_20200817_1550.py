# Generated by Django 3.0.8 on 2020-08-17 08:50

import barberback.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barberback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barbernews',
            name='bNewsImage',
            field=models.ImageField(blank=True, upload_to=barberback.models.BarberNews.upload_file, verbose_name='Картинка новости'),
        ),
    ]