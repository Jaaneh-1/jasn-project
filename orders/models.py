from django.db import models
from django.conf import settings
from catalogue.models import Produit


class Commande(models.Model):
    """
    Commande JaSN — contient la logique escrow complète.
    L'argent est bloqué jusqu'à confirmation de livraison.
    """

    class Statut(models.TextChoices):
        EN_ATTENTE   = 'en_attente',   'En attente de paiement'
        PAYE         = 'paye',         'Payé — fonds bloqués en escrow'
        EN_LIVRAISON = 'en_livraison', 'En cours de livraison'
        LIVRE        = 'livre',        'Livré — en attente de confirmation'
        CONFIRME     = 'confirme',     'Confirmé — vendeur payé'
        LITIGE       = 'litige',       'Litige ouvert'
        REMBOURSE    = 'rembourse',    'Remboursé'
        ANNULE       = 'annule',       'Annulé'

    class MethodePaiement(models.TextChoices):
        WAVE         = 'wave',         'Wave'
        ORANGE_MONEY = 'orange_money', 'Orange Money'
        CASH         = 'cash',         'Cash à la livraison'

    # Parties impliquées
    acheteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='commandes_acheteur',
        verbose_name='Acheteur'
    )
    vendeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='commandes_vendeur',
        verbose_name='Vendeur'
    )

    # Statut et paiement
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_ATTENTE,
        verbose_name='Statut'
    )
    methode_paiement = models.CharField(
        max_length=20,
        choices=MethodePaiement.choices,
        blank=True,
        verbose_name='Méthode de paiement'
    )
    montant_total = models.DecimalField(
        max_digits=12, decimal_places=0,
        verbose_name='Montant total (FCFA)'
    )

    # Livraison
    adresse_livraison = models.TextField(verbose_name='Adresse de livraison')
    telephone_livraison = models.CharField(
        max_length=20,
        verbose_name='Téléphone pour la livraison'
    )

    # Dates clés de l'escrow
    date_creation     = models.DateTimeField(auto_now_add=True, verbose_name='Date de commande')
    date_paiement     = models.DateTimeField(null=True, blank=True, verbose_name='Date de paiement')
    date_livraison    = models.DateTimeField(null=True, blank=True, verbose_name='Date de livraison')
    date_confirmation = models.DateTimeField(null=True, blank=True, verbose_name='Date de confirmation')

    # Notes
    note_acheteur = models.TextField(blank=True, verbose_name='Note de l\'acheteur')

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'
        ordering = ['-date_creation']

    def __str__(self):
        return f'Commande #{self.pk} — {self.acheteur} — {self.get_statut_display()}'

    @property
    def fonds_bloques(self):
        """L'argent est en escrow si statut entre PAYE et LIVRE"""
        return self.statut in [
            self.Statut.PAYE,
            self.Statut.EN_LIVRAISON,
            self.Statut.LIVRE,
        ]


class LigneCommande(models.Model):
    """Un produit dans une commande"""

    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes',
        verbose_name='Commande'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        verbose_name='Produit'
    )
    quantite = models.PositiveIntegerField(default=1, verbose_name='Quantité')
    prix_unitaire = models.DecimalField(
        max_digits=10, decimal_places=0,
        verbose_name='Prix unitaire (FCFA)'
    )

    class Meta:
        verbose_name = 'Ligne de commande'
        verbose_name_plural = 'Lignes de commande'

    def __str__(self):
        return f'{self.quantite}x {self.produit.nom}'

    @property
    def sous_total(self):
        return self.quantite * self.prix_unitaire


class Litige(models.Model):
    """Litige ouvert sur une commande — JaSN arbitre"""

    class Statut(models.TextChoices):
        OUVERT   = 'ouvert',   'Ouvert'
        EN_COURS = 'en_cours', 'En cours d\'examen'
        RESOLU   = 'resolu',   'Résolu'

    commande = models.OneToOneField(
        Commande,
        on_delete=models.CASCADE,
        related_name='litige',
        verbose_name='Commande'
    )
    ouvert_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Ouvert par'
    )
    motif = models.TextField(verbose_name='Motif du litige')
    statut = models.CharField(
        max_length=10,
        choices=Statut.choices,
        default=Statut.OUVERT,
        verbose_name='Statut'
    )
    resolution = models.TextField(blank=True, verbose_name='Résolution')
    date_ouverture  = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ouverture')
    date_resolution = models.DateTimeField(null=True, blank=True, verbose_name='Date de résolution')

    class Meta:
        verbose_name = 'Litige'
        verbose_name_plural = 'Litiges'

    def __str__(self):
        return f'Litige #{self.pk} — Commande #{self.commande.pk}'