from django.db import models
from django.utils import timezone


class Group(models.Model):
    group_cd = models.CharField(primary_key=True, max_length=2, null=False)
    group_nm = models.CharField(max_length=60, null=False)
    use_flg = models.CharField(max_length=2, null=False)


class User(models.Model):
    user_cd = models.CharField(primary_key=True, max_length=6, null=False)
    group_cd = models.CharField(max_length=2, null=False)
    user_id = models.CharField(unique=True, max_length=60, null=False)
    password = models.CharField(max_length=20, null=False)
    user_nm = models.CharField(max_length=60, null=False)
    mailto = models.CharField(max_length=60)
    authority_cd = models.CharField(max_length=2, null=False)
    use_flg = models.CharField(max_length=2, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)


class Question(models.Model):
    question_cd = models.CharField(primary_key=True, max_length=6, null=False)
    goup_cd = models.CharField(max_length=2, null=False)
    question = models.CharField(max_length=255, null=False)
    q_details = models.CharField(max_length=255)
    q_details_1 = models.CharField(max_length=60)
    q_details_2 = models.CharField(max_length=60)
    q_details_3 = models.CharField(max_length=60)
    q_details_4 = models.CharField(max_length=60)
    q_details_5 = models.CharField(max_length=60)
    sort_cd = models.CharField(max_length=6, null=False)
    use_flg = models.CharField(max_length=2, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

class Answer(models.Model):
    answer_cd = models.CharField(primary_key=True, max_length=6, null=False)
    user_cd = models.CharField(max_length=6, null=False)
    question_cd = models.CharField(max_length=6, null=False)
    answer = models.CharField(max_length=6)

    class Meta:
        unique_together = ('user_cd','question_cd')