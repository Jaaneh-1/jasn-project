from django.db import models
from django.conf import settings


class Categorie(models.Model):
    """Catégorie de produits — ex: Artisanat, Mode, Alimentation"""

    nom = models.CharField(max_length=100, verbose_name='Nom')
    nom_wolof = models.CharField(
        max_length=100, blank=True, verbose_name='Nom en Wolof'
    )
    slug = models.SlugField(unique=True)
    icone = models.CharField(
        max_length=10, blank=True,
        verbose_name='Emoji icône',
        help_text='Ex: 🏺 👗 🥘'
    )

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Boutique(models.Model):
    """Boutique d'un vendeur certifié JaSN"""

    vendeur = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boutique',
        verbose_name='Vendeur'
    )
    nom = models.CharField(max_length=150, verbose_name='Nom de la boutique')
    description = models.TextField(blank=True, verbose_name='Description')
    ville = models.CharField(max_length=100, verbose_name='Ville')
    adresse_repere = models.TextField(
        blank=True,
        verbose_name='Adresse par repère',
        help_text='Ex : Face à la station Total de Liberté 5'
    )
    logo = models.ImageField(
        upload_to='boutiques/logos/',
        blank=True, null=True,
        verbose_name='Logo'
    )
    est_certifiee = models.BooleanField(
        default=False,
        verbose_name='Boutique certifiée ✓'
    )
    made_in_senegal = models.BooleanField(
        default=False,
        verbose_name='Made in Sénégal 🇸🇳'
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )

    class Meta:
        verbose_name = 'Boutique'
        verbose_name_plural = 'Boutiques'

    def __str__(self):
        return f'{self.nom} — {self.ville}'


class Produit(models.Model):
    """Produit mis en vente sur JaSN"""

    boutique = models.ForeignKey(
        Boutique,
        on_delete=models.CASCADE,
        related_name='produits',
        verbose_name='Boutique'
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='produits',
        verbose_name='Catégorie'
    )

    nom = models.CharField(max_length=200, verbose_name='Nom du produit')
    nom_wolof = models.CharField(
        max_length=200, blank=True, verbose_name='Nom en Wolof'
    )
    description = models.TextField(verbose_name='Description')
    prix = models.DecimalField(
        max_digits=10, decimal_places=0,
        verbose_name='Prix (FCFA)'
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock disponible')
    image = models.ImageField(
        upload_to='produits/',
        blank=True, null=True,
        verbose_name='Image principale'
    )
    made_in_senegal = models.BooleanField(
        default=False,
        verbose_name='Made in Sénégal 🇸🇳'
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name='Produit actif'
    )
    date_ajout = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date d\'ajout'
    )

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-date_ajout']

    def __str__(self):
        return f'{self.nom} — {self.prix} FCFA'

    @property
    def en_stock(self):
        return self.stock > 0