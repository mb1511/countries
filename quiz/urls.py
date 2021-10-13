from django.urls import path

from quiz.views import QuizView

urlpatterns = [
    path("", QuizView.as_view(), name="capitals_quiz")
]
