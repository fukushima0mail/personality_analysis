from rest_framework import viewsets
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated

class QuestionViewSet(viewsets.ModelViewSet):
    '''
    質問ビュー
    '''

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_fields = ('group_cd',)
