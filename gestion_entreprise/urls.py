from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.liste_categories, name='liste_categories'),
    path('categories/<int:categorie_id>/', views.detail_categorie, name='detail_categorie'),
    path('categories/creer/', views.CreerCatégorie.as_view(), name='creer_categorie'),
    path('categories/modifier/<int:pk>/', views.ModifierCatégorie.as_view(), name='modifier_categorie'),
    path('categories/supprimer/<int:pk>/', views.SupprimerCatégorie.as_view(), name='supprimer_categorie'),

    path('produits/', views.liste_produits, name='liste_produits'),
    path('produits/<int:produit_id>/', views.detail_produit, name='detail_produit'),
    path('produits/creer/', views.CreerProduit.as_view(), name='creer_produit'),
    path('produits/modifier/<int:pk>/', views.ModifierProduit.as_view(), name='modifier_produit'),
    path('produits/supprimer/<int:pk>/', views.SupprimerProduit.as_view(), name='supprimer_produit'),

    path('stocks/', views.liste_stocks, name='liste_stocks'),
    path('stocks/<int:stock_id>/', views.detail_stock, name='detail_stock'),

    path('equipements/', views.liste_equipements, name='liste_equipements'),
    path('equipements/<int:equipement_id>/', views.detail_equipement, name='detail_equipement'),

    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('fournisseurs/<int:fournisseur_id>/', views.detail_fournisseur, name='detail_fournisseur'),

    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/<int:employe_id>/', views.detail_employe, name='detail_employe'),

    path('analyses-ventes/', views.liste_analyses_ventes, name='liste_analyses_ventes'),
    path('analyses-ventes/<int:analyse_id>/', views.detail_analyse_ventes, name='detail_analyse_ventes'),
]
