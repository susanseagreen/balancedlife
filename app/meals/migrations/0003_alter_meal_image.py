# Generated by Django 3.2.7 on 2021-10-10 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_alter_meal_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='image',
            field=models.ImageField(blank=True, max_length=255, upload_to='uploads/%Y/%m/%d'),
        ),
    ]
