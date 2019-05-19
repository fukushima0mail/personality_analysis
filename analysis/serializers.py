from rest_framework import serializers
from analysis.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'question_cd',
            'group_cd',
            'question',
            'q_details',
            'q_details_1',
            'q_details_2',
            'q_details_3',
            'q_details_4',
            'q_details_5',
            'sort_cd',
            'use_flg',
            'create_date',
            'update_date',
            )
