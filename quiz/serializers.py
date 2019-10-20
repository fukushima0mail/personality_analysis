from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from quiz.models import Question, User, Group, Answer
import uuid


class AnswerSerializer(serializers.Serializer):
    answer_cd = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=6)


class RegisterGroupValidateSerializer(serializers.ModelSerializer):
    """グループ登録用シリアライザー"""
    class Meta:
        model = Group
        fields = (
            'group_name',
        )


class RegisterUserValidateSerializer(serializers.ModelSerializer):
    """ユーザ登録用シリアライザー"""
    class Meta:
        model = User
        fields = (
            'user_name',
            'mail_address'
        )


class GetUserAnswerValidateSerializer(serializers.Serializer):
    """指定したユーザの回答取得用シリアライザー"""
    group_id = serializers.UUIDField(required=False)
    user_id = serializers.UUIDField(required=True)


class RegisterUserAnswerValidateSerializer(serializers.ModelSerializer):
    """指定したユーザの回答登録用シリアライザー"""
    class Meta:
        model = Answer
        fields = (
            'user',
            'question',
            'group',
            'answer',
            'is_correct',
            'challenge_count'
        )


class GetQuestionValidateSerializer(serializers.Serializer):
    """問題取得用シリアライザー"""
    group_id = serializers.UUIDField(required=True)
    limit = serializers.IntegerField(required=False)

    def validate_group_id(self, value):
        if not Question.objects.filter(group=value).values().exists():
            raise ValidationError(detail="group_id is not found. group_id={}".format(value))
        return value

    def validate_limit(self, value):
        if value > Question.objects.all().count():
            raise ValidationError(detail="limit is over. limit={}".format(value))
        return value


class RegisterQuestionValidateSerializer(serializers.ModelSerializer):
    """問題登録用シリアライザー"""
    class Meta:
        model = Question
        fields = (
            'group',
            'user',
            'question_type',
            'question',
            'shape_path',
            'correct',
            'choice_1',
            'choice_2',
            'choice_3',
            'choice_4'
        )
