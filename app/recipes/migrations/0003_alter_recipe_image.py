# Generated by Django 3.2.7 on 2021-09-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.CharField(max_length=255),
        ),
    ]
