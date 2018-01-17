# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 19:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0013_auto_20171005_0820'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_context', models.ForeignKey(db_column='learning_context_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='enrollment', to='db.LearningContext')),
            ],
            options={
                'db_table': 'Enrollment',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='enrollments',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='enrollment', to=settings.AUTH_USER_MODEL),
        ),
    ]
