# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsoneditor.fields.postgres_jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0020_auto_20171016_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('archived', models.NullBooleanField()),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(default={})),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default={})),
            ],
            options={
                'managed': True,
                'db_table': 'Exam',
            },
        ),
        migrations.CreateModel(
            name='ExamAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.ForeignKey(db_column='exam_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Exam')),
            ],
            options={
                'managed': True,
                'db_table': 'ExamAssociation',
            },
        ),
        migrations.CreateModel(
            name='ExamQuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.ForeignKey(db_column='exam_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Exam')),
            ],
            options={
                'managed': True,
                'db_table': 'ExamQuestionSet',
            },
        ),
        migrations.RenameModel(
            old_name='TestType',
            new_name='ExamType',
        ),
        migrations.RemoveField(
            model_name='test',
            name='questionsets',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_type',
        ),
        migrations.RemoveField(
            model_name='testassociation',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='testassociation',
            name='learning_context',
        ),
        migrations.RemoveField(
            model_name='testquestionset',
            name='question_set',
        ),
        migrations.RemoveField(
            model_name='testquestionset',
            name='test',
        ),
        migrations.RemoveField(
            model_name='result',
            name='test',
        ),
        migrations.AlterField(
            model_name='distractor',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='learningcontext',
            name='exams',
            field=models.ManyToManyField(related_name='learningcontexts', through='db.ExamAssociation', to='db.Exam'),
        ),
        migrations.AlterField(
            model_name='learningcontext',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='learningcontextterm',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='learningcontexttype',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='question',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='questionresponse',
            name='settings',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={'bookmarked': False, 'response': ''}),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='settings',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='result',
            name='settings',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={'examsettings': {}, 'questions': []}),
        ),
        migrations.AlterField(
            model_name='securityattributes',
            name='value',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='securityauditlog',
            name='params',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='term',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='user',
            name='meta',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='user',
            name='settings',
            field=jsoneditor.fields.postgres_jsonfield.JSONField(default={}),
        ),
        migrations.AlterModelTable(
            name='examtype',
            table='ExamType',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.DeleteModel(
            name='TestAssociation',
        ),
        migrations.DeleteModel(
            name='TestQuestionSet',
        ),
        migrations.AddField(
            model_name='examquestionset',
            name='question_set',
            field=models.ForeignKey(db_column='question_set_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.QuestionSet'),
        ),
        migrations.AddField(
            model_name='examassociation',
            name='learning_context',
            field=models.ForeignKey(db_column='learning_context_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.LearningContext'),
        ),
        migrations.AddField(
            model_name='exam',
            name='exam_type',
            field=models.ForeignKey(db_column='exam_type_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.ExamType'),
        ),
        migrations.AddField(
            model_name='exam',
            name='questionsets',
            field=models.ManyToManyField(related_name='exams', through='db.ExamQuestionSet', to='db.QuestionSet'),
        ),
        migrations.AddField(
            model_name='result',
            name='exam',
            field=models.ForeignKey(db_column='exam_id', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='db.Exam'),
            preserve_default=False,
        ),
    ]
