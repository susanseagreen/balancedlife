# Generated by Django 3.2.7 on 2021-10-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('date_from', models.DateTimeField(blank=True, null=True, verbose_name='date from')),
                ('date_to', models.DateTimeField(blank=True, null=True, verbose_name='date to')),
            ],
        ),
    ]
