from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('login/',       views.connexion,   name='connexion'),
    path('logout/',      views.deconnexion, name='deconnexion'),
    path('dashboard/',   views.dashboard,   name='dashboard'),
]