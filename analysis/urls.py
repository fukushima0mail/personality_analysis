from rest_framework import routers
from django.urls import path, include
from .views import QuestionViewSet, UserViewSet, GroupViewSet, AnswerView, AllAnswerView


router = routers.DefaultRouter(trailing_slash=False)
router.register('groups', GroupViewSet)
router.register('users', UserViewSet)
router.register('questions', QuestionViewSet)

urlpatterns = [
    path('users/answers', AllAnswerView.as_view()),
    path('users/<uuid:user_cd>/answers', AnswerView.as_view()),
    path("", include(router.urls)),
]