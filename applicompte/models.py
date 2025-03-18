from django.db import models
from django.contrib.auth.models import User


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
        return self.email

class PhotoUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='event_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title if self.title else f"Photo {self.id}"
    
    