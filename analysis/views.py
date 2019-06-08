from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Question, Group, User, Answer
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer, GroupSerializer
from django.http import JsonResponse

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
        res = dict(user_cd=user_cd)
        print(123)
        return JsonResponse(res)
