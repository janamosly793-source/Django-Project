from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path("play/", views.play, name="play"),
    path("result/", views.result, name="result"),
    path("scores/", views.scores, name="scores"),
]