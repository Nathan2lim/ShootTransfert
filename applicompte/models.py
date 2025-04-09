from django.db import models
from django.contrib.auth.models import User
import uuid 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255, blank=True, null=True)
    imatriculation = models.CharField(max_length=7, blank=True, null=True)
    type_user = models.IntegerField(
        default=0,
        choices=[
            (0, 'Standard'),
            (1, 'Premium'),
            (2, 'Admin'),
        ]
    )

    def __str__(self):
        return self.user.email


class PhotoUser(models.Model):
    """Photos personnelles de l'utilisateur (privées, liées à son compte)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='user_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else f"Photo {self.id}"



class ClientCode(models.Model):
    """Modèle pour gérer les codes clients."""
    code = models.CharField(max_length=50, unique=True, default=uuid.uuid4().hex[:8])  # Code aléatoire
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Activer/Désactiver un code
    user_created = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Admin qui a créé le code

    def save(self, *args, **kwargs):
        self.code = self.code.strip().lower()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.code


class TransferGallery(models.Model):
    """Gallerie de photos liée à un transfert."""
    client_code = models.OneToOneField(ClientCode, on_delete=models.CASCADE, related_name='gallery')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Galerie {self.client_code.code}"
    
    
class TransferPhoto(models.Model):
    """Photos liées à un transfert."""
    gallery = models.ForeignKey(TransferGallery, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='transfer_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id} (Galerie {self.gallery.client_code})"
