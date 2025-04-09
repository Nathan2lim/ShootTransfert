import os
import zipfile
import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

import stripe

# Modèles
from applicompte.models import ClientCode, PhotoUser, TransferGallery, TransferPhoto  # On importe uniquement les modèles nécessaires

# Formulaires
from .forms import ClientCodeForm, AddPhotosForm

# Configuration de Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'shootX/home.html')


def gallery_view(request, gallery_id):
    """Affiche les photos d'une galerie client."""
    gallery = get_object_or_404(ClientGallery, id=gallery_id)
    return render(request, "gallery.html", {"gallery": gallery})

def download_all(request, gallery_id):
    """Télécharge toutes les photos d'une galerie sous forme de fichier ZIP."""
    gallery = get_object_or_404(ClientGallery, id=gallery_id)
    zip_filename = f"photos_{gallery.client_code}.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for photo in gallery.photos.all():
            zipf.write(photo.image.path, os.path.basename(photo.image.path))

    with open(zip_path, "rb") as zipf:
        response = HttpResponse(zipf.read(), content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
        return response



@login_required
def user_photos(request):
    """Affiche les photos personnelles de l'utilisateur connecté."""
    photos = PhotoUser.objects.filter(user=request.user)
    return render(request, "shootX/user_photos.html", {"photos": photos})


logger = logging.getLogger(__name__)

def client_access(request):
    """Vue permettant aux clients d'entrer leur code pour voir leurs photos."""
    if request.method == "POST":
        code = request.POST.get("client_code", "").strip()  # Supprime les espaces avant/après
        logger.warning(f"🔍 Code saisi : '{code}'")  

        # Vérification des codes en base
        logger.warning("📌 Liste des codes en base :")
        found = False  
        for obj in ClientCode.objects.all():
            logger.warning(f"   - Code en base : '{obj.code}' (actif: {obj.is_active})")
            if obj.code.strip().lower() == code.lower():  
                found = True

        if found:
            logger.warning("✅ Correspondance trouvée en base, mais Django ne l'a pas détectée avec filter() !")

        # Recherche avec un filtre insensible à la casse
        client_code = ClientCode.objects.filter(code__iexact=code, is_active=True).first()

        if client_code:
            logger.warning(f"✅ Code trouvé via QuerySet : {client_code.code}")  

            # Recherche la galerie associée
            gallery = TransferGallery.objects.filter(client_code=client_code).first()
            if gallery:
                logger.warning(f"✅ Galerie trouvée : {gallery.id}")
                return redirect('app:transfer_gallery', gallery_id=gallery.id)

        logger.warning(f"❌ Aucun code en base ne correspond exactement au code saisi : {code}")
        return render(request, "shootX/client_access.html", {"error": "Code invalide ou inexistant"})

    return render(request, "shootX/client_access.html")


def transfer_gallery(request, gallery_id):
    """Affiche les photos d'un transfert."""
    gallery = get_object_or_404(TransferGallery, id=gallery_id)
    return render(request, "shootX/transfer_gallery.html", {"gallery": gallery})

def download_transfer_photos(request, gallery_id):
    """Télécharge toutes les photos d'un transfert en ZIP."""
    gallery = get_object_or_404(TransferGallery, id=gallery_id)
    zip_filename = f"photos_{gallery.client_code.code}.zip"
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for photo in gallery.photos.all():
            zipf.write(photo.image.path, os.path.basename(photo.image.path))

    with open(zip_path, "rb") as zipf:
        response = HttpResponse(zipf.read(), content_type="application/zip")
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
        return response

def is_admin(user):
    return user.is_staff  # Seuls les admins peuvent gérer les codes

#@login_required
#@user_passes_test(is_admin)
def code_list(request):
    """Liste des codes clients avec actions CRUD."""
    codes = ClientCode.objects.all()
    return render(request, 'shootX/admin_codes.html', {'codes': codes})

#@login_required
#@user_passes_test(is_admin)
def create_code(request):
    """Création d'un nouveau code client + création automatique de la galerie associée."""
    if request.method == 'POST':
        form = ClientCodeForm(request.POST)
        if form.is_valid():
            code = form.save(commit=False)
            code.user_created = request.user  # Enregistre l'admin (ou staff) qui crée le code
            code.save()

            # Création automatique de la galerie associée
            TransferGallery.objects.create(client_code=code)

            return redirect('app:code_list')
    else:
        form = ClientCodeForm()

    return render(request, 'shootX/create_code.html', {'form': form})

#@login_required
#@user_passes_test(is_admin)
def update_code(request, code_id):
    """Modification d'un code client existant."""
    code = get_object_or_404(ClientCode, id=code_id)
    if request.method == 'POST':
        form = ClientCodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            return redirect('app:code_list')
    else:
        form = ClientCodeForm(instance=code)
    return render(request, 'shootX/update_code.html', {'form': form})

#@login_required
#@user_passes_test(is_admin)
def delete_code(request, code_id):
    """Suppression d'un code client."""
    code = get_object_or_404(ClientCode, id=code_id)
    code.delete()
    return redirect('app:code_list')

def active_code(request, code_id):
    code = get_object_or_404(ClientCode, id=code_id)
    if code.is_active:
        code.is_active = False
    else:
        code.is_active = True
    code.save()
    return redirect('app:code_list')


def add_photos_to_gallery(request, gallery_id):
    """Page pour uploader des photos dans une TransferGallery."""
    gallery = get_object_or_404(TransferGallery, id=gallery_id)

    if request.method == 'POST':
        form = AddPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            # Récupère toutes les images envoyées
            images = request.FILES.getlist('images')
            for img in images:
                TransferPhoto.objects.create(
                    gallery=gallery,
                    image=img
                )
            messages.success(request, "Photos ajoutées avec succès !")
            return redirect('app:transfer_gallery', gallery_id=gallery_id)
    else:
        form = AddPhotosForm()

    return render(request, 'shootX/add_photos.html', {
        'form': form,
        'gallery': gallery
    })
