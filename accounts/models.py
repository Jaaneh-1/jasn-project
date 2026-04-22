from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Utilisateur JaSN — peut être Client, Vendeur, ou les deux.
    On étend le modèle Django de base pour ajouter nos champs.
    """

    class Role(models.TextChoices):
        CLIENT  = 'client',  'Client'
        VENDEUR = 'vendeur', 'Vendeur'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name='Rôle'
    )

    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Téléphone (Wave / Orange Money)'
    )

    adresse_repere = models.TextField(
        blank=True,
        verbose_name='Adresse par repère',
        help_text='Ex : Derrière la mosquée de Liberté 6, Dakar'
    )

    ville = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ville'
    )

    est_verifie = models.BooleanField(
        default=False,
        verbose_name='Compte vérifié'
    )

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date d\'inscription'
    )

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def est_vendeur(self):
        return self.role == self.Role.VENDEUR

    @property
    def est_client(self):
        return self.role == self.Role.CLIENT