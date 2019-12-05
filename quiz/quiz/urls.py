from rest_framework import routers
from django.urls import path, include
from .views import GroupView, SelectUserView, SelectUserAnswerView, QuestionView, SpecifiedQuestionView, UserView, \
    SelectUserRecordView

urlpatterns = [
    path('groups', GroupView.as_view()),
    path('users', UserView.as_view()),
    path('users/<str:user_id>', SelectUserView.as_view()),
    path('users/<str:user_id>/answers', SelectUserAnswerView.as_view()),
    path('users/<str:user_id>/current_answers_rate', SelectUserRecordView.as_view()),
    path('questions', QuestionView.as_view()),
    path('questions/<str:question_id>', SpecifiedQuestionView.as_view())
]
