from django import forms

class MultiFileField(forms.FileField):
    """Champ de formulaire Django permettant l'upload de plusieurs fichiers."""
    def to_python(self, data):
        if not data:
            return []
        return data  # data sera une liste de fichiers

    def validate(self, data):
        """Validation sur chaque fichier individuellement."""
        super().validate(data)
        for file in data:
            self.run_validators(file)