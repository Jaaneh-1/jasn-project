from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription — Client ou Vendeur"""

    email = forms.EmailField(required=True, label='Adresse email')
    telephone = forms.CharField(
        max_length=20, required=True,
        label='Téléphone (Wave / Orange Money)',
        help_text='Ex : +221 77 123 45 67'
    )
    ville = forms.CharField(max_length=100, required=True, label='Ville')
    adresse_repere = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        label='Adresse par repère',
        help_text='Ex : Derrière la mosquée de Liberté 6, Dakar'
    )
    role = forms.ChoiceField(
        choices=User.Role.choices,
        label='Je suis',
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'telephone', 'ville', 'adresse_repere', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traductions françaises des labels Django
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['username'].help_text = "Lettres, chiffres et @/./+/-/_ uniquement."
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"
        self.fields['password2'].help_text = ""
        # Classes Tailwind sur tous les champs texte
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({
                    'class': 'w-full border border-stone-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-orange-500'
                })