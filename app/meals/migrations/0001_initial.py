# Generated by Django 3.2.7 on 2021-10-16 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, default='default.png', upload_to='')),
                ('servings', models.IntegerField(blank=True, default=1, null=True)),
                ('pax_serving', models.IntegerField(blank=True, default=2, null=True, verbose_name='Pax per serving')),
                ('meal_category', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('steps', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Cooking Instructions')),
            ],
        ),
    ]
