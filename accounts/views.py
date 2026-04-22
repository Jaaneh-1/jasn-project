from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InscriptionForm
from .models import User


def inscription(request):
    """Page d'inscription Client ou Vendeur"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ! Votre compte a été créé.')
            return redirect('dashboard')
    else:
        form = InscriptionForm()

    return render(request, 'accounts/inscription.html', {'form': form})


def connexion(request):
    """Page de connexion"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')

    return render(request, 'accounts/connexion.html')


def deconnexion(request):
    """Déconnexion"""
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    """Tableau de bord — Client ou Vendeur"""
    return render(request, 'accounts/dashboard.html', {'user': request.user})