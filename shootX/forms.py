from django import forms
from applicompte.models import ClientCode
from .fields import MultiFileField

class ClientCodeForm(forms.ModelForm):
    class Meta:
        model = ClientCode
        fields = ['code', 'is_active']

from django import forms

class AddPhotosForm(forms.Form):
    images = forms.FileField(
        widget=forms.ClearableFileInput(),  # ← suppression de `multiple: True`
        required=True,
        label="Choisir une image"
    )

    def clean_images(self):
        # On retourne une liste même si un seul fichier est envoyé
        data = self.files.getlist('images')
        if not data:
            raise forms.ValidationError("Veuillez ajouter au moins une image.")
        return data