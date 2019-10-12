from rest_framework import routers
from django.urls import path, include
from .views import GroupView, SelectUserView, SelectUserAnswerView, QuestionView, SpecifiedQuestionView, UserView

# router = routers.DefaultRouter(trailing_slash=False)
# router.register('groups', GroupViewSet)
# router.register('users', UserViewSet)
# router.register('questions', QuestionViewSet)

urlpatterns = [
    path('groups', GroupView.as_view()),
    path('users', UserView.as_view()),
    path('users/<str:user_id>', SelectUserView.as_view()),
    path('users/<str:user_id>/answer', SelectUserAnswerView.as_view()),
    path('questions', QuestionView.as_view()),
    path('questions/<str:question_id>', SpecifiedQuestionView.as_view())
]
