from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def home(request):
    etapes_escrow = [
        {'icone': '🛒', 'titre': 'Acheteur commande', 'desc': 'Paiement via Wave ou Orange Money', 'couleur': 'border-amber-400'},
        {'icone': '🔒', 'titre': 'JaSN bloque les fonds', 'desc': 'Argent sécurisé en escrow', 'couleur': 'border-orange-500'},
        {'icone': '🚚', 'titre': 'Livraison effectuée', 'desc': "L'acheteur confirme la réception", 'couleur': 'border-green-500'},
        {'icone': '💰', 'titre': 'Vendeur est payé', 'desc': 'Fonds libérés automatiquement', 'couleur': 'border-blue-500'},
    ]
    return render(request, 'home.html', {'etapes_escrow': etapes_escrow})


urlpatterns = [
    path('admin/',     admin.site.urls),
    path('accounts/',  include('accounts.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('commandes/', include('orders.urls')),
    path('zendo/',     include('zendo.urls')),
    path('',           home, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)