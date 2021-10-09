# Generated by Django 3.2.7 on 2021-10-09 15:46

import app.registration.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, null=True, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('user_code', models.CharField(max_length=10, null=True)),
                ('max_left', models.PositiveIntegerField(default=10)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'registration_user',
            },
            managers=[
                ('objects', app.registration.managers.UserManager()),
            ],
        ),
    ]
