from django.db import models
from django.contrib.auth.models import User

# Modèle de Catégorie
class Catégorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.nom

# Modèle de Produit
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    composants = models.TextField()
    mode_demploi = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    prix_xof = models.DecimalField(max_digits=10, decimal_places=2)  # Prix en Franc CFA
    image = models.ImageField(upload_to='images/')
    catégorie = models.ForeignKey(Catégorie, on_delete=models.CASCADE, related_name='produits')

    def __str__(self):
        return self.nom

# Modèle de Stock
class Stock(models.Model):
    produit = models.OneToOneField(Produit, on_delete=models.CASCADE)
    quantite_disponible = models.IntegerField(default=0)

    def __str__(self):
        return f"Stock de {self.produit.nom}: {self.quantite_disponible}"

# Modèle d'Équipement
class Equipement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    localisation = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

# Modèle de Fournisseur
class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    numero_telephone = models.CharField(max_length=15)

    def __str__(self):
        return self.nom

# Modèle d'Employé
class Employé(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    numero_telephone = models.CharField(max_length=15)
    date_embauche = models.DateField()
    poste = models.CharField(max_length=100)
    salaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# Modèle d'Analyse des Ventes
class AnalyseVentes(models.Model):
    date = models.DateField()
    total_ventes = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Analyse des ventes pour {self.date}"
