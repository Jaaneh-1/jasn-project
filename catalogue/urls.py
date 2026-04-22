from django.urls import path
from . import views

urlpatterns = [
    path('',          views.catalogue,      name='catalogue'),
    path('made-in-senegal/',      views.made_in_senegal, name='made_in_senegal'),
    path('<int:produit_id>/', views.detail_produit, name='detail_produit'),
]