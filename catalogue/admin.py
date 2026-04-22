from django.contrib import admin
from .models import Categorie, Boutique, Produit


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'nom_wolof', 'icone', 'slug']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'vendeur', 'ville', 'est_certifiee', 'made_in_senegal', 'date_creation']
    list_filter   = ['est_certifiee', 'made_in_senegal', 'ville']
    search_fields = ['nom', 'vendeur__username']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'boutique', 'categorie', 'prix', 'stock', 'made_in_senegal', 'est_actif']
    list_filter   = ['made_in_senegal', 'est_actif', 'categorie']
    search_fields = ['nom', 'boutique__nom']