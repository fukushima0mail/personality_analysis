from django.db import models
from django.utils import timezone
import uuid

class Group(models.Model):
    group_cd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_nm = models.CharField(max_length=60, null=False)
    is_deleted = models.BooleanField(default=False, null=False)


class User(models.Model):
    user_cd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.CharField(unique=True, max_length=60, null=False)
    password = models.CharField(max_length=20, null=False)
    user_nm = models.CharField(max_length=60, null=False)
    mail = models.CharField(max_length=60)
    authority_cd = models.CharField(max_length=5, null=False, default=False)
    is_deleted = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)


class Question(models.Model):
    question_cd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
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
        unique_together = ('user', 'question')
