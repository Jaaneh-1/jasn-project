from django.shortcuts import render, get_object_or_404
from .models import Produit, Categorie


def catalogue(request):
    """Liste de tous les produits avec filtres"""
    produits = Produit.objects.filter(est_actif=True).select_related('boutique', 'categorie')
    categories = Categorie.objects.all()

    # Filtres
    categorie_slug = request.GET.get('categorie')
    made_in = request.GET.get('made_in')
    recherche = request.GET.get('q')

    if categorie_slug:
        produits = produits.filter(categorie__slug=categorie_slug)
    if made_in:
        produits = produits.filter(made_in_senegal=True)
    if recherche:
        produits = produits.filter(nom__icontains=recherche)

    return render(request, 'catalogue/liste.html', {
        'produits': produits,
        'categories': categories,
        'categorie_active': categorie_slug,
        'made_in': made_in,
        'recherche': recherche,
    })


def detail_produit(request, produit_id):
    """Fiche détaillée d'un produit"""
    produit = get_object_or_404(Produit, id=produit_id, est_actif=True)
    autres = Produit.objects.filter(
        boutique=produit.boutique, est_actif=True
    ).exclude(id=produit_id)[:3]

    return render(request, 'catalogue/details.html', {
        'produit': produit,
        'autres': autres,
    })





def made_in_senegal(request):
    """Page dédiée aux produits Made in Sénégal"""
    produits = Produit.objects.filter(
        est_actif=True,
        made_in_senegal=True
    ).select_related('boutique', 'categorie')

    categories = Categorie.objects.filter(
        produits__made_in_senegal=True
    ).distinct()

    # Filtre par catégorie
    categorie_slug = request.GET.get('categorie')
    if categorie_slug:
        produits = produits.filter(categorie__slug=categorie_slug)

    # Stats pour le hero
    from .models import Boutique
    total_produits  = produits.count()
    total_boutiques = Boutique.objects.filter(made_in_senegal=True).count()

    return render(request, 'catalogue/made_in_senegal.html', {
        'produits': produits,
        'categories': categories,
        'categorie_active': categorie_slug,
        'total_produits': total_produits,
        'total_boutiques': total_boutiques,
    })