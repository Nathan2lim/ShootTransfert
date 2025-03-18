from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile,PhotoUser  # Import du modèle UserProfile
from django.core.validators import RegexValidator

class UserCreationSW(UserCreationForm):
    #num = forms.IntegerField(label="Numéro spécifique")  # Champ personnalisé
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    imatriculation = forms.CharField(
        max_length=7, 
        required=False, 
        label="Imatriculation (Optional)",
        validators=[ 
            RegexValidator(r'^[a-zA-Z0-9]{7}$', 'le format de l\'imatriculation est incorrect!') 
        ]
    )
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'imatriculation')

    def save(self, commit=True):
        user = super().save(commit=False)  # Appeler la méthode parente pour créer l'utilisateur
        if commit:
            user.save()  # Sauvegarder l'utilisateur
        return user


class StandardUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['imatriculation']

class PremiumUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['imatriculation', 'type_user']

class AdminUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class PhotoUserForm(forms.ModelForm):
    class Meta:
        model = PhotoUser
        fields = ['title', 'image', 'localisation', 'description']