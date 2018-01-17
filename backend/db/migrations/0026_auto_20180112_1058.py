# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-12 17:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0025_auto_20180112_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(db_column='role_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Role')),
            ],
            options={
                'db_table': 'UserRole',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='userrole',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(db_column='role_id', related_name='user', through='db.UserRole', to='db.Role'),
        ),
    ]
