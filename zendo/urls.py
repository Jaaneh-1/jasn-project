from django.urls import path
from . import views

urlpatterns = [
    path('message/',    views.envoyer_message,    name='zendo_message'),
    path('historique/', views.historique_messages, name='zendo_historique'),
]