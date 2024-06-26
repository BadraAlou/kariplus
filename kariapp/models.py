import datetime

from django.db import models
from django.contrib.auth.models import User
import uuid

from django.utils import timezone


class Catégorie(models.Model):
    objects = None
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    composants = models.TextField()
    mode_demploi = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_xof = models.DecimalField(max_digits=10, decimal_places=2)  # Prix en Franc CFA
    image = models.ImageField(upload_to='images/')
    catégorie = models.ForeignKey('Catégorie', on_delete=models.CASCADE, related_name='produits')

    def __str__(self):
        return self.nom

class Commande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    complète = models.BooleanField(default=False)
    identifiant_transaction = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, default='Pending')  # Nouveau champ pour l'état de la commande

    def __str__(self):
        return f"Commande {self.id} par {self.utilisateur.username}"

    def annuler(self):
        if self.status == 'Pending':
            self.status = 'Cancelled'
            self.save()
            # Mise à jour ou suppression des articles de commande associés
            ArticleCommande.objects.filter(commande=self).delete()
            return True
        return False



class ArticleCommande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    quantité = models.IntegerField(default=0)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantité} de {self.produit.nom} dans la commande {self.commande.id}"


class Paiement(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    methode = models.CharField(max_length=50)
    statut = models.CharField(max_length=50)

    def __str__(self):
        return f"Paiement pour la commande {self.commande.id}"

class Panier(models.Model):
    objects = None
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"

class ArticlePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite} de {self.produit.nom} dans le panier de {self.panier.utilisateur.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    numero_telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.prenom} {self.nom}"




class Facture(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    contenu = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture pour la commande {self.commande.id}"

class Review(models.Model):
    username = models.CharField(max_length=100)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.username}"


class PasswordResetCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = datetime.timedelta(minutes=15)
        return timezone.now() > self.created_at + expiration_time