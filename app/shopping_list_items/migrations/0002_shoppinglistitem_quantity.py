# Generated by Django 3.2.7 on 2021-10-03 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list_items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglistitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
