from django.urls import path
from . import views

urlpatterns = [
    path('initier/<int:produit_id>/',      views.initier_commande,     name='initier_commande'),
    path('confirmation/<int:commande_id>/', views.confirmation_paiement, name='confirmation_paiement'),
    path('suivi/<int:commande_id>/',        views.suivi_commande,        name='suivi_commande'),
    path('mes-commandes/',                  views.mes_commandes,         name='mes_commandes'),
]