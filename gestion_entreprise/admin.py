from django.contrib import admin
from .models import Catégorie, Produit, Stock, Equipement, Fournisseur, Employé, AnalyseVentes

# Register your models here.

@admin.register(Catégorie)
class CatégorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom', 'description')

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'catégorie')
    list_filter = ('catégorie',)
    search_fields = ('nom', 'description', 'composants', 'mode_demploi')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite_disponible')
    list_filter = ('produit',)
    search_fields = ('produit__nom',)

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'localisation', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nom', 'localisation', 'description')

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse', 'email', 'numero_telephone')
    search_fields = ('nom', 'adresse', 'email', 'numero_telephone')

@admin.register(Employé)
class EmployéAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'numero_telephone', 'date_embauche', 'poste', 'salaire')
    list_filter = ('poste', 'date_embauche')
    search_fields = ('prenom', 'nom', 'email', 'numero_telephone')

@admin.register(AnalyseVentes)
class AnalyseVentesAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_ventes')
    list_filter = ('date',)
    search_fields = ('date',)
