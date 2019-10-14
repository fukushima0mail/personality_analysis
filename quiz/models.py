from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    user_name = models.CharField(max_length=30, unique=True, null=False)
    mail_address = models.CharField(unique=True, max_length=100, null=False)
    authority = models.BooleanField(max_length=5, default=False, null=False)
    correct_answer_rate = models.FloatField(null=True)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now, null=False)
    update_date = models.DateTimeField(default=timezone.now, null=False)


class Group(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    group_name = models.CharField(max_length=30, unique=True, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now, null=False)
    update_date = models.DateTimeField(default=timezone.now, null=False)


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=6, choices=(('input', 'input'), ('select', 'select')), default='select', null=False)
    question = models.CharField(max_length=255, null=False)
    shape_path = models.URLField(null=True)
    correct = models.CharField(max_length=255, null=False)
    choice_1 = models.CharField(max_length=255, null=True)
    choice_2 = models.CharField(max_length=255, null=True)
    choice_3 = models.CharField(max_length=255, null=True)
    choice_4 = models.CharField(max_length=255, null=True)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now, null=False)
    update_date = models.DateTimeField(default=timezone.now, null=False)


class Answer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=20, null=False)
    is_correct = models.BooleanField(default=False, null=False)
    challenge_count = models.IntegerField(default=0, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now, null=False)
    update_date = models.DateTimeField(default=timezone.now, null=False)
