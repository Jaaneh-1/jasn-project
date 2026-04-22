from django.contrib import admin
from .models import Commande, LigneCommande, Litige


class LigneCommandeInline(admin.TabularInline):
    """Affiche les produits directement dans la page commande"""
    model  = LigneCommande
    extra  = 0
    readonly_fields = ['sous_total']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display  = ['id', 'acheteur', 'vendeur', 'montant_total', 'statut', 'methode_paiement', 'date_creation']
    list_filter   = ['statut', 'methode_paiement']
    search_fields = ['acheteur__username', 'vendeur__username']
    readonly_fields = ['date_creation', 'date_paiement', 'date_livraison', 'date_confirmation']
    inlines = [LigneCommandeInline]


@admin.register(Litige)
class LitigeAdmin(admin.ModelAdmin):
    list_display  = ['id', 'commande', 'ouvert_par', 'statut', 'date_ouverture']
    list_filter   = ['statut']
    search_fields = ['commande__id', 'ouvert_par__username']