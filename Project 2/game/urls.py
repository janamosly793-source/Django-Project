from django.urls import path

from . import views

app_name = "game"

urlpatterns = [
    path("", views.board, name="board"),
    path("save/", views.save_score, name="save_score"),
    path("high-scores/", views.high_scores, name="high_scores"),
]