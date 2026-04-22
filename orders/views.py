from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from catalogue.models import Produit
from .models import Commande, LigneCommande


@login_required
def initier_commande(request, produit_id):
    """
    Étape 1 du tunnel — L'acheteur choisit la quantité
    et la méthode de paiement avant de confirmer.
    """
    produit = get_object_or_404(Produit, id=produit_id, est_actif=True)

    # Un vendeur ne peut pas acheter ses propres produits
    if request.user == produit.boutique.vendeur:
        messages.error(request, "Vous ne pouvez pas acheter vos propres produits.")
        return redirect('detail_produit', produit_id=produit_id)

    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        methode  = request.POST.get('methode_paiement')
        adresse  = request.POST.get('adresse_livraison')
        telephone = request.POST.get('telephone_livraison')

        if quantite > produit.stock:
            messages.error(request, f"Stock insuffisant. Seulement {produit.stock} disponibles.")
            return redirect('initier_commande', produit_id=produit_id)

        # Créer la commande
        commande = Commande.objects.create(
            acheteur=request.user,
            vendeur=produit.boutique.vendeur,
            statut=Commande.Statut.EN_ATTENTE,
            methode_paiement=methode,
            montant_total=produit.prix * quantite,
            adresse_livraison=adresse,
            telephone_livraison=telephone,
        )

        # Ajouter la ligne
        LigneCommande.objects.create(
            commande=commande,
            produit=produit,
            quantite=quantite,
            prix_unitaire=produit.prix,
        )

        return redirect('confirmation_paiement', commande_id=commande.id)

    return render(request, 'orders/initier.html', {'produit': produit})


@login_required
def confirmation_paiement(request, commande_id):
    """
    Étape 2 — Résumé de la commande avant paiement.
    L'acheteur voit le montant et confirme.
    """
    commande = get_object_or_404(
        Commande, id=commande_id, acheteur=request.user, statut=Commande.Statut.EN_ATTENTE
    )

    if request.method == 'POST':
        # Simuler le paiement — en production ici on appelle l'API Wave/Orange Money
        commande.statut = Commande.Statut.PAYE
        commande.date_paiement = timezone.now()
        commande.save()

        # Décrémenter le stock
        for ligne in commande.lignes.all():
            ligne.produit.stock -= ligne.quantite
            ligne.produit.save()

        messages.success(request, "Paiement confirmé ! Vos fonds sont sécurisés en escrow.")
        return redirect('suivi_commande', commande_id=commande.id)

    return render(request, 'orders/confirmation.html', {'commande': commande})


@login_required
def suivi_commande(request, commande_id):
    """
    Étape 3 — Suivi en temps réel du statut de la commande.
    L'acheteur peut confirmer la livraison ici.
    """
    commande = get_object_or_404(Commande, id=commande_id)

    # Seul l'acheteur ou le vendeur peut voir la commande
    if request.user not in [commande.acheteur, commande.vendeur]:
        messages.error(request, "Accès non autorisé.")
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')

        # Acheteur confirme la réception
        if action == 'confirmer_livraison' and request.user == commande.acheteur:
            if commande.statut == Commande.Statut.EN_LIVRAISON:
                commande.statut = Commande.Statut.CONFIRME
                commande.date_confirmation = timezone.now()
                commande.save()
                messages.success(request, "Livraison confirmée ! Le vendeur va être payé.")

        # Vendeur marque en livraison
        elif action == 'marquer_livraison' and request.user == commande.vendeur:
            if commande.statut == Commande.Statut.PAYE:
                commande.statut = Commande.Statut.EN_LIVRAISON
                commande.date_livraison = timezone.now()
                commande.save()
                messages.success(request, "Commande marquée en livraison.")

        # Ouvrir un litige
        elif action == 'ouvrir_litige':
            if commande.statut not in [Commande.Statut.CONFIRME, Commande.Statut.ANNULE]:
                commande.statut = Commande.Statut.LITIGE
                commande.save()
                messages.warning(request, "Litige ouvert. JaSN va examiner votre dossier.")

        return redirect('suivi_commande', commande_id=commande.id)

    return render(request, 'orders/suivi.html', {'commande': commande})


@login_required
def mes_commandes(request):
    """Liste des commandes de l'utilisateur connecté"""
    if request.user.est_vendeur:
        commandes = Commande.objects.filter(vendeur=request.user).order_by('-date_creation')
    else:
        commandes = Commande.objects.filter(acheteur=request.user).order_by('-date_creation')

    return render(request, 'orders/mes_commandes.html', {'commandes': commandes})