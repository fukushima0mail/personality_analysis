from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, APIException
from .models import Group, User, Answer, Question
from .serializers import GetUserAnswerValidateSerializer, RegisterUserAnswerValidateSerializer, \
    GetQuestionValidateSerializer, RegisterGroupValidateSerializer, RegisterUserValidateSerializer, \
    RegisterQuestionValidateSerializer
from django.http import HttpResponse
import json


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     グループビューセット
#     """
#
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     ユーザビューセット
#     """
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     filter_fields = ('group',)
#
#
# class QuestionViewSet(viewsets.ModelViewSet):
#     """
#     質問ビューセット
#     """
#
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#     filter_fields = ('group',)


class GroupView(APIView):
    """/group"""

    def get(self, request):
        """グループ取得"""
        res = Group.objects.filter(is_deleted=False).values('group_id', 'group_name')
        if not res.exists():
            raise NotFound()

        return Response(res)

    def post(self, request):
        """グループ登録"""
        param = json.loads(request.body)
        data = RegisterGroupValidateSerializer(data=param)
        data.is_valid(raise_exception=True)
        Group.objects.create(**data.validated_data)
        return HttpResponse(status=204)


class UserView(APIView):
    """/user"""

    def get(self, request):
        """ユーザ取得"""
        res = User.objects.filter(is_deleted=False).values(
            'user_id', 'user_name', 'mail_address', 'authority', 'correct_answer_rate')
        if not res.exists():
            raise NotFound()

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
        try:
            val = User.objects.get(user_id=user_id, is_deleted=False)
        except User.DoesNotExist:
            raise NotFound()

        res = dict()
        res['user_id'] = val.user_id
        res['user_name'] = val.user_name
        res['mail_address'] = val.mail_address
        res['authority'] = val.authority
        res['correct_answer_rate'] = val.correct_answer_rate
        return Response(res)


class SelectUserAnswerView(APIView):
    """/users/{id}/answer"""

    def get(self, request, user_id):
        """指定したユーザの回答を取得 Todo:作成中"""
        group_id = request.GET.get('group_id')
        data = GetUserAnswerValidateSerializer(data=dict(user_id=user_id, group_id=group_id))
        data.is_valid(raise_exception=True)

        try:
            res = Answer.objects.get(**data.validated_data)
        except Answer.DoesNotExist:
            raise NotFound()
        return HttpResponse(res)

    def post(self, request, user_id):
        """指定したユーザの回答を登録"""
        data = json.loads(request.body)
        data = RegisterUserAnswerValidateSerializer(data=dict(**data, user_id=user_id))
        data.is_valid(raise_exception=True)

        try:
            Answer.objects.create(**data.validated_data)
        except Exception as e:
            raise APIException(e)

        return HttpResponse(status=204)


class QuestionView(APIView):
    """/questions"""

    def get(self, request):
        """問題取得"""
        group_id = request.GET.get('group_id')
        limit = request.GET.get('limit', 1)

        data = GetQuestionValidateSerializer(data=dict(group_id=group_id, limit=limit))
        data.is_valid(raise_exception=True)
        res = Question.objects.filter(group_id=data.validated_data['group_id']).values(
            'question_id', 'group_id', 'user_id', 'question_type', 'question',
            'shape_path', 'correct', 'choice_1', 'choice_2', 'choice_3', 'choice_4'
        )[:limit]

        if not res.exists():
            raise NotFound()

        return Response(res)

    def post(self, request):
        """問題登録"""
        param = json.loads(request.body)
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
