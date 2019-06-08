from rest_framework import serializers
from analysis.models import Question, User, Group, Answer

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

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'answer_cd',
            'user',
            'question',
            'answer',
            )
