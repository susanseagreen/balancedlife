# Generated by Django 3.2.7 on 2021-11-26 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient_categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientcategory',
            name='order',
            field=models.IntegerField(default=1, max_length=2),
        ),
    ]
