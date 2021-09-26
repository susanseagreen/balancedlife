# Generated by Django 3.2.7 on 2021-09-26 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredient_categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('servings', models.IntegerField(blank=True, default=1, null=True)),
                ('pax_serving', models.IntegerField(blank=True, default=2, null=True, verbose_name='Pax per serving')),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('steps', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Cooking Instructions')),
                ('code_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe', to='ingredient_categories.ingredientcategory', verbose_name='Category')),
            ],
        ),
    ]
