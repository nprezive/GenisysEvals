# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-05 14:02
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsoneditor.fields.postgres_jsonfield


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('picture_id', models.CharField(blank=True, default='', max_length=12)),
                ('student_id', models.CharField(blank=True, default='', max_length=9)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'User',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Distractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('legacy_question_id', models.IntegerField(blank=True, null=True)),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('correct', models.NullBooleanField()),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(blank=True, null=True)),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'Distractor',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'Enrollment',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LearningContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('short_code', models.CharField(blank=True, max_length=25, null=True)),
                ('number', models.CharField(blank=True, max_length=25, null=True)),
                ('active', models.NullBooleanField()),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(blank=True, null=True)),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'LearningContext',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LearningContextStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
                ('child_context', models.ForeignKey(db_column='learning_context_child_id', default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_context', to='db.LearningContext')),
                ('parent_context', models.ForeignKey(db_column='learning_context_parent_id', default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='child_context', to='db.LearningContext')),
            ],
            options={
                'db_table': 'LearningContextStructure',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LearningContextTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('override_start_date', models.DateTimeField(blank=True, null=True)),
                ('override_end_date', models.DateTimeField(blank=True, null=True)),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
                ('learning_context', models.ForeignKey(db_column='learning_context_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.LearningContext')),
            ],
            options={
                'db_table': 'LearningContextTerm',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LearningContextType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'LearningContextType',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(blank=True, null=True)),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'Question',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(blank=True, null=True)),
                ('graded', models.NullBooleanField()),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(default="{response: ''}")),
                ('question', models.ForeignKey(db_column='question_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Question')),
            ],
            options={
                'db_table': 'QuestionResponse',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'QuestionSet',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionSetAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_context', models.ForeignKey(db_column='learning_context_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.LearningContext')),
                ('question_set', models.ForeignKey(db_column='question_set_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.QuestionSet')),
            ],
            options={
                'db_table': 'QuestionSetAssociation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionSetQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(db_column='question_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='questionsets', to='db.Question')),
                ('question_set', models.ForeignKey(db_column='question_set_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='questionset_questions', to='db.QuestionSet')),
            ],
            options={
                'db_table': 'QuestionSetQuestion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('template', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'QuestionType',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('score_sent', models.DateTimeField(blank=True, null=True)),
                ('archived', models.NullBooleanField()),
            ],
            options={
                'db_table': 'Result',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('rights', jsoneditor.fields.postgres_jsonfield.JSONField(default='[]')),
            ],
            options={
                'db_table': 'Role',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SecurityAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.CharField(max_length=100)),
                ('value', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='SecurityAuditLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('url', models.URLField()),
                ('action', models.CharField(blank=True, default='', max_length=100)),
                ('params', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('location', models.CharField(blank=True, max_length=80, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('size', models.SmallIntegerField(blank=True, null=True)),
                ('require_checkin', models.NullBooleanField()),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Site',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SiteComputer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('certificate', models.TextField(blank=True, null=True)),
                ('active', models.NullBooleanField()),
                ('site', models.ForeignKey(db_column='site_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Site')),
            ],
            options={
                'db_table': 'SiteComputer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('term_code', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'Term',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('archived', models.NullBooleanField()),
                ('settings', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
                ('meta', jsoneditor.fields.postgres_jsonfield.JSONField(default='{}')),
            ],
            options={
                'db_table': 'Test',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TestAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.ForeignKey(db_column='test_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Test')),
                ('learning_context', models.ForeignKey(db_column='learning_context_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.LearningContext')),
            ],
            options={
                'db_table': 'TestAssociation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TestQuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_set', models.ForeignKey(db_column='question_set_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.QuestionSet')),
                ('test', models.ForeignKey(db_column='test_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Test')),
            ],
            options={
                'db_table': 'TestQuestionSet',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'TestType',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=256)),
                ('expires', models.DateTimeField()),
                ('rights', jsoneditor.fields.postgres_jsonfield.JSONField(default='[]')),
                ('restrictions', jsoneditor.fields.postgres_jsonfield.JSONField(default="{ 'ip': 'Any', 'host':'Any', 'certificate':'Any', 'user_id': 0, 'learningcontext_id': 0 }")),
            ],
        ),
        migrations.AddField(
            model_name='test',
            name='questionsets',
            field=models.ManyToManyField(related_name='tests', through='db.TestQuestionSet', to='db.QuestionSet'),
        ),
        migrations.AddField(
            model_name='test',
            name='test_type',
            field=models.ForeignKey(db_column='test_type_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.TestType'),
        ),
        migrations.AddField(
            model_name='result',
            name='site',
            field=models.ForeignKey(db_column='site_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Site'),
        ),
        migrations.AddField(
            model_name='result',
            name='test',
            field=models.ForeignKey(db_column='test_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Test'),
        ),
        migrations.AddField(
            model_name='result',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questionset',
            name='questions',
            field=models.ManyToManyField(related_name='questions', through='db.QuestionSetQuestion', to='db.Question'),
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='result',
            field=models.ForeignKey(db_column='result_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Result'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.ForeignKey(db_column='question_type_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.QuestionType'),
        ),
        migrations.AddField(
            model_name='learningcontextterm',
            name='term',
            field=models.ForeignKey(db_column='term_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.Term'),
        ),
        migrations.AddField(
            model_name='learningcontext',
            name='exams',
            field=models.ManyToManyField(related_name='learningcontexts', through='db.TestAssociation', to='db.Test'),
        ),
        migrations.AddField(
            model_name='learningcontext',
            name='learning_context_type',
            field=models.ForeignKey(db_column='learning_context_type_id', on_delete=django.db.models.deletion.DO_NOTHING, to='db.LearningContextType'),
        ),
        migrations.AddField(
            model_name='learningcontext',
            name='question_sets',
            field=models.ManyToManyField(through='db.QuestionSetAssociation', to='db.QuestionSet'),
        ),

        migrations.AddField(
            model_name='distractor',
            name='question',
            field=models.ForeignKey(db_column='question_id', on_delete=django.db.models.deletion.DO_NOTHING, related_name='distractors', to='db.Question'),
        ),

        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
