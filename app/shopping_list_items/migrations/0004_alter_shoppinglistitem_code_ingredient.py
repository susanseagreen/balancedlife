# Generated by Django 3.2.7 on 2021-10-02 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
        ('shopping_list_items', '0003_alter_shoppinglistitem_code_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglistitem',
            name='code_ingredient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shopping_list_item', to='ingredients.ingredient', verbose_name='Ingredient'),
        ),
    ]
