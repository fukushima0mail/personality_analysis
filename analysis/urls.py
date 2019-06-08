from rest_framework import routers
from django.urls import path, include
from .views import QuestionViewSet, UserViewSet, GroupViewSet, AnswerView


router = routers.DefaultRouter(trailing_slash=True)
router.register('groups', GroupViewSet)
router.register('users', UserViewSet)
router.register('questions', QuestionViewSet)

urlpatterns = [
    path('users/<uuid:user_cd>/answers', AnswerView.as_view(), name="get"),
    path("", include(router.urls)),
]