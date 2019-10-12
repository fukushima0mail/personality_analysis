from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_name = models.ForeignKey(unique=True, max_length=20)
    mail_address = models.CharField(unique=True, max_length=100, null=False)
    authority_id = models.CharField(max_length=5, default='user', null=False)
    correct_answer_rate = models.FloatField(null=True,)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now, null=False)
    update_date = models.DateTimeField(default=timezone.now, null=False)


class Group(models.Model):
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group_name = models.CharField(max_length=20, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now, null=False)
    update_date = models.DateTimeField(default=timezone.now, null=False)


class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    question = models.CharField(max_length=255, null=False)
    q_details = models.CharField(max_length=255)
    sort_cd = models.CharField(max_length=6, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)


class Answer(models.Model):
    answer_cd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=6)

    class Meta:
        unique_together = (('user', 'question'),)
