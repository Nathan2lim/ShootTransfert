from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import *
from applicompte.models import *

##################################################
# TESTS DES MODÈLES
##################################################

class ClientCodeModelTest(TestCase):
    def setUp(self):
        self.user_admin = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpass',
            is_staff=True
        )
        # Création d'un code client
        self.client_code = ClientCode.objects.create(
            code='TESTCODE',
            is_active=True,
            user_created=self.user_admin
        )

    def test_code_str(self):
        """Vérifie que la représentation en str du modèle correspond au code."""
        self.assertEqual(str(self.client_code), 'testcode') 
        # Attention: dans votre code, vous faites un `strip().lower()` dans la méthode save()
        # Donc ça devient 'testcode' une fois enregistré.


class TransferGalleryModelTest(TestCase):
    def setUp(self):
        # On crée un ClientCode
        self.client_code = ClientCode.objects.create(code='galcode', is_active=True)
        # On crée la galerie
        self.gallery = TransferGallery.objects.create(client_code=self.client_code)

    def test_gallery_str(self):
        self.assertIn('galerie galcode', str(self.gallery).lower())


class TransferPhotoModelTest(TestCase):
    def setUp(self):
        # On crée un code client et sa galerie
        self.client_code = ClientCode.objects.create(code='mycode', is_active=True)
        self.gallery = TransferGallery.objects.create(client_code=self.client_code)

        # On simule un fichier image
        self.test_image = SimpleUploadedFile(
            "test.jpg",
            b"\x47\x49\x46\x38\x39\x61",  # octets d’un GIF minimal, par exemple
            content_type="image/gif"
        )
    
    def test_transfer_photo_creation(self):
        """Test de la création d'une photo liée à un transfert."""
        photo = TransferPhoto.objects.create(
            gallery=self.gallery,
            image=self.test_image
        )
        self.assertTrue(photo.id is not None)
        self.assertEqual(photo.gallery, self.gallery)

    def test_transfer_photo_str(self):
        photo = TransferPhoto.objects.create(
            gallery=self.gallery,
            image=self.test_image
        )
        self.assertIn('Photo', str(photo))
        self.assertIn('mycode', str(photo))


class PhotoUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pass123')
        self.test_image = SimpleUploadedFile(
            "userphoto.jpg",
            b"\x47\x49\x46\x38\x39\x61",  # octets d’un GIF minimal
            content_type="image/gif"
        )

    def test_photo_user_creation(self):
        photo_user = PhotoUser.objects.create(
            user=self.user,
            title='Photo test',
            image=self.test_image
        )
        self.assertEqual(photo_user.title, 'Photo test')
        self.assertEqual(photo_user.user, self.user)
        self.assertIn('userphoto', photo_user.image.name)  # Vérifie simplement que le nom contient 'userphoto'


##################################################
# TESTS DES VUES
##################################################

class ClientAccessViewTest(TestCase):
    def setUp(self):
        self.client_ = Client()
        # Création de quelques codes
        self.code_actif = ClientCode.objects.create(code='actif', is_active=True)
        self.code_inactif = ClientCode.objects.create(code='inactif', is_active=False)

        # Galerie associée au code actif
        self.gallery_actif = TransferGallery.objects.create(client_code=self.code_actif)
        # Galerie associée au code inactif
        self.gallery_inactif = TransferGallery.objects.create(client_code=self.code_inactif)

    def test_client_access_view_ok(self):
        """
        Teste la vue `client_access` avec un code actif valide.
        On vérifie qu’on est bien redirigé vers la page `transfer_gallery`.
        """
        response = self.client_.post(
            reverse('app:home'),
            {'client_code': 'actif'}
        )
        # doit rediriger vers transfer_gallery
        self.assertEqual(response.status_code, 302)
        self.assertIn('/gallery/', response.url)

    def test_client_access_view_invalid_code(self):
        """
        Teste la vue `client_access` avec un code invalide.
        On vérifie qu’on reste sur la même page avec un message d’erreur.
        """
        response = self.client_.post(
            reverse('app:home'),
            {'client_code': 'foo'}
        )
        self.assertEqual(response.status_code, 200)  # on reste sur la page
        self.assertContains(response, "Code invalide ou inexistant")

    def test_client_access_view_inactive_code(self):
        """
        Teste la vue `client_access` avec un code inactif.
        On vérifie qu’on ne redirige pas vers la galerie.
        """
        response = self.client_.post(
            reverse('app:home'),
            {'client_code': 'inactif'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Code invalide ou inexistant")


class CodeListViewTest(TestCase):
    def setUp(self):
        self.client_ = Client()
        # Création d'un user staff pour se connecter
        self.staff_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        # On logge cet user
        self.client_.login(username='admin', password='adminpass')

        # Quelques codes
        self.code1 = ClientCode.objects.create(code='code1', is_active=True)
        self.code2 = ClientCode.objects.create(code='code2', is_active=False)

    def test_code_list_view(self):
        """Vérifie que la vue liste les codes et retourne un 200."""
        response = self.client_.get(reverse('app:code_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'code1')
        self.assertContains(response, 'code2')


class CreateCodeViewTest(TestCase):
    def setUp(self):
        self.client_ = Client()
        # Création d'un user staff pour se connecter
        self.staff_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        self.client_.login(username='admin', password='adminpass')

    def test_create_code_valid(self):
        """Test de la création d'un code via la vue create_code."""
        response = self.client_.post(
            reverse('app:create_code'),
            {'code': 'moncode', 'is_active': True}
        )
        # doit rediriger
        self.assertEqual(response.status_code, 302)
        # On vérifie que le code a été créé
        self.assertTrue(ClientCode.objects.filter(code='moncode').exists())
        # On vérifie aussi que la TransferGallery a été créée
        created_code = ClientCode.objects.get(code='moncode')
        self.assertTrue(
            TransferGallery.objects.filter(client_code=created_code).exists()
        )

    def test_create_code_invalid_form(self):
        """Test si le formulaire est invalide (ex. champ manquant)."""
        response = self.client_.post(
            reverse('app:create_code'),
            {'code': ''}  # champ code vide
        )
        # reste sur la même page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce champ est obligatoire")


class UpdateCodeViewTest(TestCase):
    def setUp(self):
        self.client_ = Client()
        # Création d'un user staff pour se connecter
        self.staff_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        self.client_.login(username='admin', password='adminpass')

        self.code = ClientCode.objects.create(code='mycode', is_active=True)

    def test_update_code(self):
        """Test la mise à jour d'un code."""
        response = self.client_.post(
            reverse('app:update_code', args=[self.code.id]),
            {'code': 'updatedcode', 'is_active': False}
        )
        self.assertEqual(response.status_code, 302)
        self.code.refresh_from_db()
        self.assertEqual(self.code.code, 'updatedcode')
        self.assertFalse(self.code.is_active)


class DeleteCodeViewTest(TestCase):
    def setUp(self):
        self.client_ = Client()
        # Création d'un user staff pour se connecter
        self.staff_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        self.client_.login(username='admin', password='adminpass')
        self.code = ClientCode.objects.create(code='mycode', is_active=True)

    def test_delete_code(self):
        response = self.client_.post(
            reverse('app:delete_code', args=[self.code.id])
        )
        # Normalement c’est une requête GET dans votre code, mais on peut tester POST
        self.assertEqual(response.status_code, 302)
        # On vérifie que le code n’existe plus
        self.assertFalse(ClientCode.objects.filter(code='mycode').exists())


class ActiveCodeViewTest(TestCase):
    def setUp(self):
        self.client_ = Client()
        # Création d'un user staff pour se connecter
        self.staff_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        self.client_.login(username='admin', password='adminpass')
        self.code = ClientCode.objects.create(code='mycode', is_active=True)

    def test_active_code(self):
        """Vérifie que la vue toggle l’état is_active."""
        response = self.client_.get(
            reverse('app:active_code', args=[self.code.id])
        )
        self.assertEqual(response.status_code, 302)
        self.code.refresh_from_db()
        self.assertFalse(self.code.is_active)

        # On refait un toggle pour le repasser actif
        response = self.client_.get(
            reverse('app:active_code', args=[self.code.id])
        )
        self.code.refresh_from_db()
        self.assertTrue(self.code.is_active)


##################################################
# TESTS D'AJOUT DE PHOTOS (ex: add_photos_to_gallery)
##################################################

class AddPhotosToGalleryViewTest(TestCase):
    def setUp(self):
        self.client_ = Client()
        # On crée un user staff (pour l’exemple)
        self.staff_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        self.client_.login(username='admin', password='adminpass')
        # On crée un code + galerie
        self.client_code = ClientCode.objects.create(code='gallerycode', is_active=True)
        self.gallery = TransferGallery.objects.create(client_code=self.client_code)
        self.url = reverse('app:add_photos_to_gallery', kwargs={'gallery_id': self.gallery.id})

    def test_add_photos_view_get(self):
        response = self.client_.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Choisir une image')

    def test_add_photos_view_post(self):
        """On simule le POST avec une image."""
        uploaded_file = SimpleUploadedFile(
            "test.jpg",
            b"\x47\x49\x46\x38\x39\x61",  # octets d’un GIF minimal
            content_type="image/gif"
        )

        response = self.client_.post(
            self.url,
            {'images': uploaded_file}
        )
        self.assertEqual(response.status_code, 302)
        # On vérifie qu’une TransferPhoto a bien été créée
        self.assertEqual(self.gallery.photos.count(), 1)

        # Vérifier que le message de succès a bien été configuré
        # Django test framework ne gère pas direct messages, 
        # mais on peut vérifier la redirection ou d’autres éléments.