from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Interface admin pour les utilisateurs JaSN"""

    list_display = ['username', 'email', 'role', 'ville', 'telephone', 'est_verifie', 'date_creation']
    list_filter  = ['role', 'est_verifie', 'ville']
    search_fields = ['username', 'email', 'telephone']

    # Ajouter nos champs personnalisés dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations JaSN', {
            'fields': ('role', 'telephone', 'adresse_repere', 'ville', 'est_verifie')
        }),
    )