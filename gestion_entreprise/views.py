from django.shortcuts import render, redirect, get_object_or_404
from .models import Catégorie, Produit, Stock, Equipement, Fournisseur, Employé, AnalyseVentes
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

# Vue pour afficher la liste des catégories
@login_required
def liste_categories(request):
    categories = Catégorie.objects.all()
    return render(request, 'liste_categories.html', {'categories': categories})

# Vue pour afficher les détails d'une catégorie
@login_required
def detail_categorie(request, categorie_id):
    categorie = get_object_or_404(Catégorie, pk=categorie_id)
    return render(request, 'detail_categorie.html', {'categorie': categorie})

# Vue pour créer une nouvelle catégorie
class CreerCatégorie(CreateView):
    model = Catégorie
    fields = ['nom', 'description', 'image']
    template_name = 'creer_categorie.html'

    def get_success_url(self):
        return reverse('liste_categories')

# Vue pour mettre à jour une catégorie existante
class ModifierCatégorie(UpdateView):
    model = Catégorie
    fields = ['nom', 'description', 'image']
    template_name = 'modifier_categorie.html'

    def get_success_url(self):
        return reverse('liste_categories')

# Vue pour supprimer une catégorie
class SupprimerCatégorie(DeleteView):
    model = Catégorie
    template_name = 'supprimer_categorie.html'

    def get_success_url(self):
        return reverse('liste_categories')


# Vue pour afficher la liste des produits
@login_required
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'liste_produits.html', {'produits': produits})

# Vue pour afficher les détails d'un produit
@login_required
def detail_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    return render(request, 'detail_produit.html', {'produit': produit})

# Vue pour créer un nouveau produit
class CreerProduit(CreateView):
    model = Produit
    fields = ['nom', 'description', 'composants', 'mode_demploi', 'prix', 'prix_xof', 'image', 'catégorie']
    template_name = 'creer_produit.html'

    def get_success_url(self):
        return reverse('liste_produits')

# Vue pour mettre à jour un produit existant
class ModifierProduit(UpdateView):
    model = Produit
    fields = ['nom', 'description', 'composants', 'mode_demploi', 'prix', 'prix_xof', 'image', 'catégorie']
    template_name = 'modifier_produit.html'

    def get_success_url(self):
        return reverse('liste_produits')

# Vue pour supprimer un produit
class SupprimerProduit(DeleteView):
    model = Produit
    template_name = 'supprimer_produit.html'

    def get_success_url(self):
        return reverse('liste_produits')


# Vue pour afficher la liste des stocks
@login_required
def liste_stocks(request):
    stocks = Stock.objects.all()
    return render(request, 'liste_stocks.html', {'stocks': stocks})

# Vue pour afficher les détails d'un stock
@login_required
def detail_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    return render(request, 'detail_stock.html', {'stock': stock})


# Vue pour afficher la liste des équipements
@login_required
def liste_equipements(request):
    equipements = Equipement.objects.all()
    return render(request, 'liste_equipements.html', {'equipements': equipements})

# Vue pour afficher les détails d'un équipement
@login_required
def detail_equipement(request, equipement_id):
    equipement = get_object_or_404(Equipement, pk=equipement_id)
    return render(request, 'detail_equipement.html', {'equipement': equipement})


# Vue pour afficher la liste des fournisseurs
@login_required
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'liste_fournisseurs.html', {'fournisseurs': fournisseurs})

# Vue pour afficher les détails d'un fournisseur
@login_required
def detail_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    return render(request, 'detail_fournisseur.html', {'fournisseur': fournisseur})


# Vue pour afficher la liste des employés
@login_required
def liste_employes(request):
    employes = Employé.objects.all()
    return render(request, 'liste_employes.html', {'employes': employes})

# Vue pour afficher les détails d'un employé
@login_required
def detail_employe(request, employe_id):
    employe = get_object_or_404(Employé, pk=employe_id)
    return render(request, 'detail_employe.html', {'employe': employe})


# Vue pour afficher la liste des analyses de ventes
@login_required
def liste_analyses_ventes(request):
    analyses = AnalyseVentes.objects.all()
    return render(request, 'liste_analyses_ventes.html', {'analyses': analyses})

# Vue pour afficher les détails d'une analyse de ventes
@login_required
def detail_analyse_ventes(request, analyse_id):
    analyse = get_object_or_404(AnalyseVentes, pk=analyse_id)
    return render(request, 'detail_analyse_ventes.html', {'analyse': analyse})
