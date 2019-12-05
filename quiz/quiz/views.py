from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, APIException
from .models import Group, User, Answer, Question
from .serializers import GetUserAnswerValidateSerializer, RegisterUserAnswerValidateSerializer, \
    GetQuestionValidateSerializer, RegisterGroupValidateSerializer, RegisterUserValidateSerializer, \
    RegisterQuestionValidateSerializer
from django.http import HttpResponse
import json
import pandas
import random

TO_PERCENTAGE = 100
NUMBER_OF_DIGITS = 3

class GroupView(APIView):
    """/group"""

    def get(self, request):
        """グループ取得"""
        res = Group.objects.filter(is_deleted=False).values('group_id', 'group_name')
        if not res.exists():
            raise NotFound(detail="The target record is not found.")

        return Response(res)

    def post(self, request):
        """グループ登録"""
        param = json.loads(request.body)
        data = RegisterGroupValidateSerializer(data=param)
        data.is_valid(raise_exception=True)
        Group.objects.create(**data.validated_data)
        return HttpResponse(status=204)


class UserView(APIView):
    """/users"""

    def get(self, request):
        """ユーザ取得"""
        res = User.objects.filter(is_deleted=False).values(
            'user_id', 'user_name', 'mail_address', 'authority', 'correct_answer_rate')
        if not res.exists():
            raise NotFound(detail="The target record is not found.")

        return Response(res)

    def post(self, request):
        """ユーザ情報登録"""
        param = json.loads(request.body)
        data = RegisterUserValidateSerializer(data=param)
        data.is_valid(raise_exception=True)

        User.objects.create(**data.validated_data)
        return HttpResponse(status=204)


class SelectUserView(APIView):
    """/users/{id}"""

    def get(self, request, user_id):
        """ユーザ情報取得"""
        val = User.objects.get(user_id=user_id, is_deleted=False)
        if not val.exists():
            raise NotFound(detail="The target record is not found.")

        res = dict()
        res['user_id'] = val.user_id
        res['user_name'] = val.user_name
        res['mail_address'] = val.mail_address
        res['authority'] = val.authority
        res['correct_answer_rate'] = val.correct_answer_rate
        return Response(res)


class SelectUserRecordView(APIView):
    """/users/{id}/record"""

    def get(self, request, user_id):
        """指定したユーザの成績を取得"""
        param = dict(user_id=user_id)

        data = GetUserAnswerValidateSerializer(data=param)
        data.is_valid(raise_exception=True)

        answers = Answer.objects.filter(
            **data.validated_data, is_deleted=False).select_related('group').order_by('challenge_count').values(
            'group__group_name', 'is_correct', 'challenge_count')
        if not answers.exists():
            raise NotFound(detail="The target record is not found.")

        res = self._Make_response(answers)
        return Response(res)

    def _Make_response(self, answers):
        df = pandas.DataFrame(answers)
        response = OrderedDict()
        response['total_count'] = df['is_correct'].count()
        response['correct_answer_count'] = df['is_correct'].sum()
        response['correct_answer_rate'] = round(df['is_correct'].mean(), NUMBER_OF_DIGITS) * TO_PERCENTAGE

        correct_answer_rates = df.groupby('challenge_count').mean().to_dict().get('is_correct')
        correct_answer_counts = df.groupby('challenge_count').sum().to_dict().get('is_correct')
        total_counts = df.groupby('challenge_count').count().to_dict().get('is_correct')

        count = 1
        detail_list = list()
        while True:
            # チャレンジ回数ごとの問題数、正解数、平均正解率を計算する
            correct_answer_rate = correct_answer_rates.get(count, None)
            correct_answer_count = correct_answer_counts.get(count, None)
            total_count = total_counts.get(count, None)

            if correct_answer_rate is None:
                break
            detail = dict()
            detail['challenge_count'] = count
            detail['total_count'] = total_count
            detail['correct_answer_count'] = int(correct_answer_count)
            detail['correct_answer_rate'] = round(correct_answer_rate, NUMBER_OF_DIGITS) * TO_PERCENTAGE
            detail['correct_answer_rate2'] = correct_answer_rate
            detail['group_name'] = list(df[df['challenge_count'] == count].get('group__group_name').to_dict().values()).pop()
            detail_list.append(detail)
            count += 1

        response['detail'] = detail_list

        return response


class SelectUserAnswerView(APIView):
    """/users/{id}/answers"""

    def post(self, request, user_id):
        """指定したユーザの回答を登録し、結果を返却する"""
        data = json.loads(request.body)
        data = RegisterUserAnswerValidateSerializer(
            data=dict(question=data.get('question_id'),
                      group=data.get('group_id'),
                      user=user_id,
                      answer=data.get('answer'),
                      challenge_count=data.get('challenge_count')))
        data.is_valid(raise_exception=True)

        try:
            question_id = data.validated_data.get('question').question_id
            query = Question.objects.get(question_id=question_id)
        except Exception as e:
            raise APIException(e)

        res = dict()
        res['result'] = True if query.correct == data.validated_data.get('answer') else False
        try:
            Answer.objects.create(**data.validated_data, is_correct=res['result'])
        except Exception as e:
            raise APIException(e)

        return Response(res)


class QuestionView(APIView):
    """/questions"""

    def get(self, request):
        """問題取得"""
        group_id = request.GET.get('group_id')
        degree = request.GET.get('degree')
        limit = request.GET.get('limit', 5)

        data = GetQuestionValidateSerializer(data=dict(group_id=group_id, limit=limit, degree=degree))
        data.is_valid(raise_exception=True)
        group_id = data.validated_data['group_id']
        degree = data.validated_data['degree']
        query = Question.objects.filter(group_id=group_id, degree=degree, is_deleted=0).values(
            'question_id', 'group_id', 'user_id', 'question_type', 'question',
            'shape_path', 'correct', 'choice_1', 'choice_2', 'choice_3', 'choice_4'
        )
        if query.count() < data.validated_data['limit']:
            data.validated_data['limit'] = query.count()
        if not query.exists():
            raise NotFound(detail="The target record is not found.")

        response = random.sample(list(query), data.validated_data['limit'])
        return Response(response)

    def post(self, request):
        """問題登録"""
        param = json.loads(request.body)
        param['group'] = param.get('group_id')
        param['user'] = param.get('user_id')
        data = RegisterQuestionValidateSerializer(data=param)
        data.is_valid(raise_exception=True)

        try:
            Question.objects.create(**data.validated_data)
        except Exception as e:
            raise APIException(detail=e)

        return HttpResponse(status=204)


class SpecifiedQuestionView(APIView):
    """/questions/{question_id}"""

    def get(self, request, user_id):
        # Todo: 問題更新API
        pass

    def post(self, request, user_id):
        # Todo: 問題削除API
        pass
