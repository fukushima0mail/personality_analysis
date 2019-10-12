from django.db import models
from rest_framework import serializers
from quiz.models import Question, User, Group, Answer
import uuid


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'group_cd',
            'group_nm',
            )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_cd',
            'group',
            'user_id',
            'password',
            'user_nm',
            'authority_cd',
            )

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'question_cd',
            'group',
            'question',
            'q_details',
            'sort_cd',
            )

class AnswerSerializer(serializers.Serializer):
    answer_cd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=6)
