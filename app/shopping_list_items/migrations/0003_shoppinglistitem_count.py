# Generated by Django 3.2.7 on 2021-09-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list_items', '0002_auto_20210918_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglistitem',
            name='count',
            field=models.IntegerField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]
