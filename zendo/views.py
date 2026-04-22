import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Conversation, Message


def get_or_create_conversation(request):
    """Récupère ou crée une conversation pour cet utilisateur/session"""
    if request.user.is_authenticated:
        conv, _ = Conversation.objects.get_or_create(
            utilisateur=request.user,
            defaults={}
        )
    else:
        if not request.session.session_key:
            request.session.create()
        conv, _ = Conversation.objects.get_or_create(
            session_key=request.session.session_key,
            utilisateur=None,
            defaults={}
        )
    return conv


@require_POST
def envoyer_message(request):
    """
    Reçoit le message de l'utilisateur et retourne
    la réponse de Zendo en JSON.
    """
    try:
        data = json.loads(request.body)
        message_utilisateur = data.get('message', '').strip()

        if not message_utilisateur:
            return JsonResponse({'erreur': 'Message vide'}, status=400)

        # Récupérer/créer la conversation
        conversation = get_or_create_conversation(request)

        # Sauvegarder le message de l'utilisateur
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.USER,
            contenu=message_utilisateur
        )

        # ── MODE SIMULATION ──────────────────────────────────────────
        # Remplacer ce bloc par l'appel API Anthropic quand les crédits
        # seront disponibles.
        message_lower = message_utilisateur.lower()

        if 'escrow' in message_lower or 'séquestre' in message_lower:
            texte_reponse = (
                "L'escrow JaSN bloque votre argent en sécurité jusqu'à "
                "la livraison confirmée. Yëgël na — vous êtes protégé ! 🔒"
            )
        elif any(m in message_lower for m in ['wave', 'orange', 'paiement', 'payer']):
            texte_reponse = (
                "JaSN accepte Wave, Orange Money et le cash à la livraison. "
                "Pas besoin de carte bancaire ! 💙🟠"
            )
        elif any(m in message_lower for m in ['livraison', 'adresse', 'livrer']):
            texte_reponse = (
                "Pour la livraison, indiquez un repère local comme "
                "'Derrière la mosquée de Liberté 6'. "
                "On s'adapte à votre quartier ! 📍"
            )
        elif any(m in message_lower for m in ['litige', 'problème', 'arnaque', 'remboursement']):
            texte_reponse = (
                "En cas de problème, JaSN intervient comme arbitre neutre. "
                "Cliquez sur 'Signaler un problème' dans votre commande "
                "et on s'en occupe ! ⚖️"
            )
        elif any(m in message_lower for m in ['vendeur', 'boutique', 'vendre']):
            texte_reponse = (
                "Pour devenir vendeur, créez un compte Vendeur et complétez "
                "votre boutique. La certification JaSN vous donnera "
                "le badge de confiance ! 🏪"
            )
        elif any(m in message_lower for m in ['commande', 'acheter', 'achat']):
            texte_reponse = (
                "Pour commander : choisissez un produit, cliquez Acheter, "
                "choisissez votre paiement (Wave ou Orange Money), "
                "et confirmez. Votre argent est sécurisé jusqu'à la livraison ! 🛒"
            )
        elif any(m in message_lower for m in ['made in', 'sénégal', 'local', 'artisan']):
            texte_reponse = (
                "La section 'Made in Sénégal' valorise nos artisans locaux — "
                "paniers, bazin, parfums thiouraye... "
                "Achetez local, soutenez notre économie ! 🇸🇳"
            )
        elif any(m in message_lower for m in ['bonjour', 'salut', 'hello', 'asalaa']):
            texte_reponse = (
                "Asalaa maalekum ! 👋 Je suis Zendo, votre assistant JaSN. "
                "Je peux vous aider avec l'escrow, les paiements, "
                "les livraisons ou les litiges. Que voulez-vous savoir ?"
            )
        else:
            texte_reponse = (
                "Je suis Zendo, l'assistant JaSN ! 😊 "
                "Je peux vous aider sur : l'escrow, Wave/Orange Money, "
                "les livraisons, les litiges ou devenir vendeur. "
                "Quelle est votre question ?"
            )
        # ── FIN MODE SIMULATION ──────────────────────────────────────

        # Sauvegarder la réponse de Zendo
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            contenu=texte_reponse
        )

        return JsonResponse({'reponse': texte_reponse})

    except Exception as e:
        return JsonResponse({'erreur': str(e)}, status=500)


def historique_messages(request):
    """Retourne les derniers messages de la conversation en cours"""
    conversation = get_or_create_conversation(request)
    messages = conversation.messages.order_by('date')[:20]
    data = [
        {'role': msg.role, 'contenu': msg.contenu}
        for msg in messages
    ]
    return JsonResponse({'messages': data})