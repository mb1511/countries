from django.urls import path, include


urlpatterns = [
    path("quiz/", include("quiz.urls")),
]
