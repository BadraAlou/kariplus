from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='accueil'),  # Page d'accueil
    path('produits/', views.produits, name='produits'),  # Afficher les produits
    path('commande/<int:produit_id>/', views.order, name='order'),  # Afficher une commande spécifique
    path('a-propos/', views.about_us, name='about_us'),  # Page "À propos"
    path('produit/<int:produit_id>/ajouter-panier/', views.ajouter_au_panier, name='ajouter_au_panier'),  # Ajouter un produit au panier
    path('voir-panier/', views.voir_panier, name='voir_panier'),  # Voir le panier
    path('modifier-quantite-panier/<int:article_id>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),  # Modifier la quantité d'un article dans le panier
    path('supprimer-du-panier/<int:article_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),  # Supprimer un article du panier
    path('connexion/', views.connexion, name='connexion'),  # Page de connexion
    path('deconnexion/', views.deconnexion, name='deconnexion'),  # Page de déconnexion
    path('profil-utilisateur/', views.profil_utilisateur, name='profil_utilisateur'),  # Profil utilisateur
    path('modifier-profil/', views.modifier_profil, name='modifier_profil'),  # Modifier le profil utilisateur
    path('passer-commande/', views.passer_commande, name='passer_commande'),  # Passer une commande
    path('inscription/', views.inscription, name='inscription'),  # Inscription utilisateur
    path('generer-facture/<int:commande_id>/', views.generer_facture, name='generer_facture'),
    path('get_panier_total_produits/', views.get_panier_total_produits, name='get_panier_total_produits'),
    path('accounts/login/', views.connexion, name='connexion'),  # Référencement de l'ancienne URL pour la compatibilité
    path('review/create/', views.create_review, name='create_review'),
    path('confirmation-commande/', views.confirmation_commande, name='confirmation_commande'),
    path('historique_commandes/', views.historique_commandes, name='historique_commandes'),
    path('commande-directe/<int:produit_id>/', views.commande_directe, name='commande_directe'),
    path('connexion/', views.connexion, name='connexion'),
    path('contacts/', views.contacts, name='contacts'),
    path('send-reset-code/', views.send_reset_code, name='send_reset_code'),
    path('confirm-reset-code/', views.confirm_reset_code, name='confirm_reset_code'),
path('annuler_commande/<int:commande_id>/', views.annuler_commande, name='annuler_commande'),

]
