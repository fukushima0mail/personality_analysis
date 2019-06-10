from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question, Group, User, Answer
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer, GroupSerializer
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
import uuid
import json

class GroupViewSet(viewsets.ModelViewSet):
    '''
    グループビューセット
    '''

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    '''
    ユーザビューセット
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('group',)

class QuestionViewSet(viewsets.ModelViewSet):
    '''
    質問ビューセット
    '''

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_fields = ('group',)

class AllAnswerView(APIView):

    def get(self, request):
        param = Answer.objects.all().values()
        return Response(param)

class AnswerView(APIView):

    def get(self, request, user_cd):
        param = Answer.objects.filter(user=user_cd).values()        
        return Response(param)

    def post(self, request, user_cd):
        data = json.loads(request.body)

        for val in data:
            serializer = AnswerSerializer(data=val)
            serializer.is_valid(raise_exception=True)

            try:
                Answer.objects.get_or_create(user_id=val["user_id"],
                                             question_id=val["question_id"],
                                             answer=val["answer"])
            except IntegrityError:
                # 複合ユニークキーが登録済みの場合は更新
                target = Answer.objects.filter(user_id=val["user_id"],
                                               question_id=val["question_id"])
                target.update(answer=val["answer"])
                
        return HttpResponse(status=200)

    def put(self, request, user_cd):
        data = json.loads(request.body)
        serializer = AnswerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        param = dict(user_id=data["user_id"], question_id=data["question_id"])
        target = Answer.objects.filter(**param)
        target.update(answer=data["answer"])
        return HttpResponse(status=200)
