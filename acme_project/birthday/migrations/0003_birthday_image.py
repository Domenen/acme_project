# Generated by Django 3.2.16 on 2024-05-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthday', '0002_alter_birthday_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthday',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Фото'),
        ),
    ]
