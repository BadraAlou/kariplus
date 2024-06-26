from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Catégorie, Produit, Commande, ArticleCommande, Paiement, Panier, ArticlePanier, UserProfile, Review


class CatégorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'afficher_image')
    search_fields = ('nom', 'description')
    list_per_page = 20

    def afficher_image(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return "Pas d'image disponible"

    afficher_image.short_description = 'Image'

admin.site.register(Catégorie, CatégorieAdmin)


class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'catégorie')
    list_filter = ('catégorie',)
    search_fields = ('nom', 'description')
    list_per_page = 20

admin.site.register(Produit, ProduitAdmin)


class CommandeAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'date_commande', 'complète', 'status')
    list_filter = ('date_commande', 'complète', 'status')
    search_fields = ('utilisateur__username',)
    list_per_page = 20
    readonly_fields = ('date_commande',)

admin.site.register(Commande, CommandeAdmin)


class ArticleCommandeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'get_nom_produit', 'quantité', 'date_ajout')
    search_fields = ('commande__utilisateur__username', 'produit__nom')
    list_per_page = 20

    def get_nom_produit(self, obj):
        if obj.produit:
            return obj.produit.nom
        return "Produit manquant"

    get_nom_produit.short_description = 'Produit'

admin.site.register(ArticleCommande, ArticleCommandeAdmin)


class PaiementAdmin(admin.ModelAdmin):
    list_display = ('commande', 'montant', 'date_paiement', 'methode', 'statut')
    list_filter = ('date_paiement', 'methode', 'statut')
    search_fields = ('commande__utilisateur__username',)
    list_per_page = 20

admin.site.register(Paiement, PaiementAdmin)


class PanierAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'date_creation')
    search_fields = ('utilisateur__username',)
    list_per_page = 20
    readonly_fields = ('date_creation',)

admin.site.register(Panier, PanierAdmin)


class ArticlePanierAdmin(admin.ModelAdmin):
    list_display = ('panier', 'produit', 'quantite', 'date_ajout')
    search_fields = ('panier__utilisateur__username', 'produit__nom')
    list_per_page = 20

admin.site.register(ArticlePanier, ArticlePanierAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profils'
    readonly_fields = ('user',)

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    list_per_page = 20

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('username', 'review', 'created_at')
    search_fields = ('username', 'review')
    list_per_page = 20

admin.site.register(Review, ReviewAdmin)
