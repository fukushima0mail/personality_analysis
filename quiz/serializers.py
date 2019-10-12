from django.db import models
from rest_framework import serializers
from quiz.models import Question, User, Group, Answer
import uuid


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'group_id',
            'group_name',
            )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'user_name',
            'mail_address',
            'authority',
            'correct_answer_rate'
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


class RegistGroupValidateSerializer(serializers.ModelSerializer):
    """グループ登録用シリアライザー"""
    class Meta:
        model = Group
        fields = (
            'group_name',
        )


class RegistUserValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_name',
            'mail_address'
        )



class GetUserAnswerValidateSerializer(serializers.ModelSerializer):
    """指定したユーザの回答取得用シリアライザー"""
    class Meta:
        model = Answer
        fields = (
            'group_name'
        )


class RegistUserAnswerValidateSerializer(serializers.ModelSerializer):
    """指定したユーザの回答登録用シリアライザー"""
    class Meta:
        model = Answer
        fields = (
            'question_id',
            'answer',
            'is_correct',
            'challenge_count'
        )


class GetQuestionValidateSerializer(serializers.ModelSerializer):
    """問題取得用シリアライザー"""
    class Meta:
        model = Question
        fields = (
            'group_id',
            'limit'
        )
