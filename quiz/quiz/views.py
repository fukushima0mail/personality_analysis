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


class SelectUserCurrentAnswerRateView(APIView):
    """/users/{id}/current_answers_rate"""

    def get(self, request, user_id):
        """指定したユーザの回答率を取得"""
        param = dict(user_id=user_id)
        if request.GET.get('group_id'):
            param['group_id'] = request.GET.get('group_id')

        data = GetUserAnswerValidateSerializer(data=param)
        data.is_valid(raise_exception=True)

        answers = Answer.objects.filter(
            **data.validated_data, is_deleted=False).order_by('challenge_count').values(
            'group_id', 'is_correct', 'challenge_count')
        if not answers.exists():
            raise NotFound(detail="The target record is not found.")

        res = self._Make_response(answers)
        return Response(res)

    def _Make_response(self, answers):
        df = pandas.DataFrame(answers)

        response = OrderedDict()
        response['correct_answer_rate'] = df['is_correct'].mean()

        average_per_count = df.groupby('challenge_count').mean().to_dict().get('is_correct')
        # print('average_per_count={}'.format(average_per_count))
        count = 1
        detail_list = list()
        while True:
            # チャレンジ回数ごとの平均点を計算する
            correct_answer_rate = average_per_count.get(count, None)
            if correct_answer_rate is None:
                break
            detail = dict()
            detail['challenge_count'] = count
            detail['correct_answer_rate'] = float(correct_answer_rate)
            # print("df[df['challenge_count'] == count]")
            # print(df[df['challenge_count'] == count])
            # print('df = {}'.format(df))
            detail['group_id'] = list(df[df['challenge_count'] == count].get('group_id').to_dict().values()).pop()
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
