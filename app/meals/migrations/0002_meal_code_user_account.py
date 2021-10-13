# Generated by Django 3.2.7 on 2021-10-13 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meals', '0001_initial'),
        ('user_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='code_user_account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='meal', to='user_accounts.useraccountname'),
        ),
    ]
