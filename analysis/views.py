from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question, Group, User, Answer
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer, GroupSerializer
from django.http import JsonResponse, HttpResponse
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

class AnswerView(APIView):

    def get(self, request, user_cd):
        param = Answer.objects.filter(user=user_cd).values()        
        return Response(param)

    def post(self, request, user_cd):
        data = json.loads(request.body)
        serializer = AnswerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        item, create = Answer.objects.get_or_create(data)
        if not create:
            return HttpResponse("Registered", status=400)
        return HttpResponse(status=200)
