# Generated by Django 2.1 on 2019-10-17 14:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('answer', models.CharField(max_length=20)),
                ('is_correct', models.BooleanField(default=False)),
                ('challenge_count', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=30, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_type', models.CharField(choices=[('input', 'input'), ('select', 'select')], default='select', max_length=6)),
                ('question', models.CharField(max_length=255)),
                ('shape_path', models.URLField(null=True)),
                ('correct', models.CharField(max_length=255)),
                ('choice_1', models.CharField(max_length=255, null=True)),
                ('choice_2', models.CharField(max_length=255, null=True)),
                ('choice_3', models.CharField(max_length=255, null=True)),
                ('choice_4', models.CharField(max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Group')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30, unique=True)),
                ('mail_address', models.CharField(max_length=100, unique=True)),
                ('authority', models.BooleanField(default=False, max_length=5)),
                ('correct_answer_rate', models.FloatField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.User'),
        ),
        migrations.AddField(
            model_name='answer',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Group'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.User'),
        ),
    ]
