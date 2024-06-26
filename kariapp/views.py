import os
from decimal import Decimal, ROUND_HALF_UP
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import register
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.platypus.flowables import Image

from .forms import CustomUserCreationForm, UserProfileForm
from .models import Commande, ArticleCommande, Produit, Panier, ArticlePanier, Catégorie, UserProfile, PasswordResetCode


# Vues pour afficher les pages
def home(request):
    context = {'panier_total_produits': get_panier_total_produits(request.user)}
    return render(request, 'accueil.html', context)


def produits(request):
    categories = Catégorie.objects.all()
    produits_par_categories = {catégorie: Produit.objects.filter(catégorie=catégorie) for catégorie in categories}
    context = {
        'produits_par_categories': produits_par_categories,
        'panier_total_produits': get_panier_total_produits(request.user)
    }
    return render(request, 'produits.html', context)


def about_us(request):
    return render(request, 'a_propos.html')


def connexion(request):
    error_message = None
    login_attempts = request.session.get('login_attempts', 0)

    if request.user.is_authenticated:
        return redirect('accueil')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['login_attempts'] = 0  # reset login attempts
            return redirect('accueil')
        else:
            login_attempts += 1
            request.session['login_attempts'] = login_attempts
            error_message = "Nom d'utilisateur ou mot de passe incorrect."

    return render(request, 'connexion.html', {
        'error_message': error_message,
        'login_attempts': login_attempts,
    })


def send_reset_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code, created = PasswordResetCode.objects.get_or_create(user=user)
            reset_code.code = generate_reset_code()  # Générer un code de quatre chiffres
            reset_code.created_at = timezone.now()
            reset_code.save()

            # Envoyer l'email
            send_mail(
                'Réinitialisation du mot de passe',
                f'Vous recevez ce message en réponse à votre demande de réinitialisation du mot de passe de votre '
                f'compte. Votre code de réinitialisation est: {reset_code.code}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return redirect('confirm_reset_code')  # Assurez-vous que cette URL existe
        except User.DoesNotExist:
            # Vous pouvez afficher un message d'erreur ici
            pass
    return render(request, 'send_reset_code.html')


import random
import string


def generate_reset_code(length=4):
    return ''.join(random.choices(string.digits, k=length))


def confirm_reset_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            reset_code = PasswordResetCode.objects.get(code=code)
            if reset_code.is_expired():
                reset_code.delete()
                return render(request, 'confirm_reset_code.html', {'error': 'Code expiré.'})

            # Vérifier si les champs de mot de passe sont présents dans la requête POST
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 and new_password2:
                form = SetPasswordForm(reset_code.user,
                                       {'new_password1': new_password1, 'new_password2': new_password2})
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    reset_code.delete()
                    return redirect('connexion')
                else:
                    # Si le formulaire n'est pas valide, renvoyer à la page avec les erreurs
                    return render(request, 'confirm_reset_code.html', {
                        'error': 'Les mots de passe ne correspondent pas ou ne respectent pas les exigences.'})

            return render(request, 'confirm_reset_code.html', {'valid_code': True, 'code': code})
        except PasswordResetCode.DoesNotExist:
            return render(request, 'confirm_reset_code.html', {'error': 'Code invalide.'})

    return render(request, 'confirm_reset_code.html')


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Envoi de l'e-mail de confirmation
            subject = 'Confirmation d\'inscription'
            message = 'Bienvenue sur KariPlus ! Vous vous êtes inscrit avec succès. Nous sommes ravis de vous compter parmi nous.'
            sender_email = 'youssoufd163@gmail.com'
            user_email = user.email

            email = EmailMessage(subject, message, sender_email, [user_email])
            email.send()

            return redirect('accueil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})


# Vue pour la page de déconnexion
def deconnexion(request):
    logout(request)
    return redirect('accueil')


# Vues liées au profil utilisateur
@login_required
def profil_utilisateur(request):
    profil = UserProfile.objects.get(user=request.user)
    return render(request, 'profil_utilisateur.html', {'profil': profil})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Commande
from django.db.models import Sum, F

@login_required
def historique_commandes(request):
    commandes_with_totals = Commande.objects.filter(utilisateur=request.user).annotate(
        total_prix=Sum(F('articlecommande__produit__prix') * F('articlecommande__quantité'))
    ).order_by('-date_commande')

    return render(request, 'historique_commandes.html', {'commandes_with_totals': commandes_with_totals})



# Vues liées au panier
@login_required
def afficher_panier(request):
    panier_utilisateur, _ = Panier.objects.get_or_create(utilisateur=request.user)
    articles_panier = ArticlePanier.objects.filter(panier=panier_utilisateur)
    total_prix = articles_panier.aggregate(total_prix=Sum(F('quantite') * F('produit__prix')))['total_prix']
    return render(request, 'panier.html', {'articles_panier': articles_panier, 'total_prix': total_prix})


@login_required
def modifier_quantite_panier(request, article_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        article_panier = ArticlePanier.objects.get(pk=article_id)
        article_panier.quantite = quantite
        article_panier.save()
    return redirect('afficher_panier')


@login_required
def supprimer_du_panier(request, article_id):
    article_panier = get_object_or_404(ArticlePanier, pk=article_id)
    if request.method == 'POST':
        article_panier.delete()
    return redirect('afficher_panier')


# Vue pour afficher une commande spécifique
def order(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    context = {'produit': produit}
    return render(request, 'commande_directe.html', context)


# Vue pour ajouter un produit au panier
@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier_utilisateur, _ = Panier.objects.get_or_create(utilisateur=request.user)
    ArticlePanier.objects.create(panier=panier_utilisateur, produit=produit)
    return redirect('produits')


# Vue pour afficher le panier de l'utilisateur
@login_required
def afficher_panier(request):
    panier_utilisateur, _ = Panier.objects.get_or_create(utilisateur=request.user)
    articles_panier = ArticlePanier.objects.filter(panier=panier_utilisateur)
    total_prix = articles_panier.aggregate(total_prix=Sum(F('quantite') * F('produit__prix')))['total_prix']
    return render(request, 'panier.html', {'articles_panier': articles_panier, 'total_prix': total_prix})


@login_required
def voir_panier(request):
    panier_utilisateur, _ = Panier.objects.get_or_create(utilisateur=request.user)
    articles_panier = ArticlePanier.objects.filter(panier=panier_utilisateur)

    # Calcul du prix total en utilisant aggregate avec Sum
    total_prix = articles_panier.aggregate(total_prix=Sum(F('quantite') * F('produit__prix')))['total_prix'] or 0

    return render(request, 'voir_panier.html', {'articles_panier': articles_panier, 'total_prix': total_prix})


@login_required
def modifier_quantite_panier(request, article_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        article_panier = ArticlePanier.objects.get(pk=article_id)
        article_panier.quantite = quantite
        article_panier.save()
    return redirect('voir_panier')


@login_required
def supprimer_du_panier(request, article_id):
    article_panier = get_object_or_404(ArticlePanier, pk=article_id)
    if request.method == 'POST':
        article_panier.delete()
    return redirect('voir_panier')


@login_required
def modifier_profil(request):
    profil = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('profil_utilisateur')
    else:
        form = UserProfileForm(instance=profil)
    return render(request, 'modifier_profil.html', {'form': form})


def get_panier_total_produits(user):
    if user.is_authenticated:
        panier_utilisateur, _ = Panier.objects.get_or_create(utilisateur=user)
        total_produits = \
            ArticlePanier.objects.filter(panier=panier_utilisateur).aggregate(total_produits=Sum('quantite'))[
                'total_produits']
        return total_produits or 0
    return 0  # Retourne 0 pour les utilisateurs non authentifiés


# Vue pour la page "À propos"
def about_us(request):
    return render(request, 'a_propos.html')


@register.filter
def multiply(value, arg):
    return value * arg



# dans views.py
from django.shortcuts import render, redirect
from .forms import ReviewForm


def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')  # Redirige vers la vue qui liste toutes les critiques
    else:
        form = ReviewForm()

    return render(request, 'contacts.html', {'form': form})


@login_required
def historique_commandes(request):
    commandes = Commande.objects.filter(utilisateur=request.user).order_by('-date_commande')
    commandes_with_totals = []

    for commande in commandes:
        total_prix = sum(article.produit.prix * article.quantité for article in commande.articlecommande_set.all())
        commandes_with_totals.append({
            'commande': commande,
            'total_prix': total_prix
        })

    return render(request, 'historique_commandes.html', {'commandes_with_totals': commandes_with_totals})

@login_required
def passer_commande(request):
    panier_utilisateur, _ = Panier.objects.get_or_create(utilisateur=request.user)
    articles_panier = ArticlePanier.objects.filter(panier=panier_utilisateur)

    if request.method == 'POST':
        # Création de la commande
        commande = Commande.objects.create(utilisateur=request.user, complète=False)

        # Ajouter chaque article du panier à la commande
        for article_panier in articles_panier:
            ArticleCommande.objects.create(
                commande=commande,
                produit=article_panier.produit,
                quantité=article_panier.quantite
            )

        # Marquer la commande comme complète
        commande.complète = True
        commande.save()

        # Vider le panier de l'utilisateur
        articles_panier.delete()

        # Génération de la facture en PDF
        pdf_buffer = generate_invoice(commande)

        # Envoi de l'e-mail de confirmation avec la facture en pièce jointe
        subject = 'Confirmation de commande'
        message = 'Votre commande a été passée avec succès ! Veuillez trouver votre facture en pièce jointe.'
        sender_email = 'votre_email@example.com'
        user_email = request.user.email

        email = EmailMessage(subject, message, sender_email, [user_email])
        email.attach(f'facture_{commande.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

        # Redirection vers une page de confirmation de commande
        messages.success(request, 'Votre commande a été passée avec succès.')
        return redirect('confirmation_commande')

    total_prix = articles_panier.aggregate(total_prix=Sum(F('quantité') * F('produit__prix')))['total_prix']
    return render(request, 'passer_commande.html', {'articles_panier': articles_panier, 'total_prix': total_prix})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

@login_required
def annuler_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, utilisateur=request.user)

    if commande.status == 'Pending':
        commande.status = 'Cancelled'
        commande.save()  # Enregistrer la mise à jour

        # Envoi de l'e-mail de confirmation d'annulation
        subject = 'Annulation de commande'
        message = 'Votre commande a été annulée avec succès.'
        sender_email = 'votre_email@example.com'
        user_email = request.user.email

        email = EmailMessage(subject, message, sender_email, [user_email])
        email.send()

        # Suppression de la commande après annulation
        commande.delete()

        messages.success(request, 'Votre commande a été annulée et supprimée de l\'historique avec succès.')
    else:
        messages.error(request, 'Cette commande ne peut pas être annulée.')

    return redirect('historique_commandes')
@login_required
def commande_directe(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))

        # Création de la commande avec le produit sélectionné
        commande = Commande.objects.create(utilisateur=request.user, complète=True)
        ArticleCommande.objects.create(commande=commande, produit=produit, quantité=quantite)

        # Génération de la facture en PDF et autres actions nécessaires
        pdf_buffer = generate_invoice(commande)

        # Envoi de l'e-mail de confirmation avec la facture en pièce jointe
        subject = 'Confirmation de commande'
        message = 'Votre commande a été passée avec succès ! Veuillez trouver votre facture en pièce jointe.'
        sender_email = 'votre_email@example.com'
        user_email = request.user.email

        email = EmailMessage(subject, message, sender_email, [user_email])
        email.attach(f'facture_{commande.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
        email.send()

        # Redirection vers une page de confirmation de commande
        messages.success(request, 'Votre commande a été passée avec succès.')
        return redirect('confirmation_commande')

    return render(request, 'commande_directe.html', {'produit': produit})


def confirmation_commande(request):
    derniere_commande = Commande.objects.filter(utilisateur=request.user).order_by('-id').first()
    return render(request, 'confirmation_commande.html', {'commande': derniere_commande})


def generate_invoice(commande):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Chemin du logo de l'entreprise
    logo_path = os.path.join(settings.STATIC_ROOT, 'img', 'logo.jpg')

    # En-tête de la facture et cadre
    p.setStrokeColor(colors.HexColor("#27ae60"))
    p.setFillColor(colors.HexColor("#27ae60"))
    p.rect(40, height - 70, width - 80, 30, fill=1)  # Encadrer et remplir le titre INVOICE
    p.setFillColor(colors.whitesmoke)
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 65, "FACTURE")

    # Informations de l'entreprise
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.black)
    p.drawString(40, height - 100, "KariPlus")
    p.drawString(40, height - 130, "Bamako, Mali")
    p.drawString(40, height - 145, "Téléphone: 00223 72 88 26 25")
    p.drawString(40, height - 160, "Email: kariplus@gmail.com")

    # Informations de la commande et de l'utilisateur
    p.drawString(40, height - 220, f"Client: {commande.utilisateur.username}")
    p.drawString(40, height - 235, f"Commande #{commande.id}")
    if commande.date_commande:
        p.drawString(40, height - 250, f"Date: {commande.date_commande.strftime('%Y-%m-%d %H:%M:%S')}")

    # Tableau des articles commandés
    articles_commande = ArticleCommande.objects.filter(commande=commande)
    data = [["Produit", "Quantité", "Prix unitaire (FCFA)", "Total (FCFA)"]]
    for article in articles_commande:
        produit = article.produit
        quantite = article.quantité
        prix_unitaire = Decimal(produit.prix).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_article = (Decimal(produit.prix) * quantite).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        data.append([produit.nom, quantite, f"{prix_unitaire:.2f}", f"{total_article:.2f}"])

    table = Table(data, colWidths=[200, 100, 120, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#27ae60")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 40, height - 400)

    # Insérer le logo en dessous du cadre
    if os.path.exists(logo_path):
        p.drawImage(logo_path, width - 6 * cm, height - 7 * cm, width=4 * cm, height=4 * cm, preserveAspectRatio=True,
                    mask='auto')

    # Pied de page avec le prix total et remerciements
    total_prix = sum(Decimal(article.produit.prix) * article.quantité for article in articles_commande)
    y = height - 420 - len(articles_commande) * 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, f"Prix total: {total_prix:.2f} FCFA")

    p.setLineWidth(1)
    p.line(40, y - 10, width - 40, y - 10)

    p.setFont("Helvetica", 10)
    p.drawString(40, y - 30, "Merci pour votre achat !")
    p.drawString(40, y - 50, "Pour toute question, contactez-nous à kariplus.com")

    # Sauvegarder et fermer le PDF
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


def generer_facture(request, commande_id):
    # Obtenez la commande et les articles commandés
    commande = get_object_or_404(Commande, id=commande_id, utilisateur=request.user)
    articles_commande = ArticleCommande.objects.filter(commande=commande)

    if not articles_commande.exists():
        return HttpResponse("Oups une erreur s'est produite.", content_type='text/plain')

    # Calculer le total de la commande
    total_prix = sum(Decimal(article.produit.prix) * article.quantité for article in articles_commande)

    # Créer la réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="facture_{commande_id}.pdf"'

    # Initialiser le canvas PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Chemin du logo de l'entreprise
    logo_path = os.path.join('kariapp', 'static', 'img', 'logo.jpg')

    # En-tête de la facture et cadre
    p.setStrokeColor(colors.HexColor("#27ae60"))
    p.setFillColor(colors.HexColor("#27ae60"))
    p.rect(40, height - 70, width - 80, 30, fill=1)  # Encadrer et remplir le titre FACTURE
    p.setFillColor(colors.whitesmoke)
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2, height - 65, "FACTURE")

    # Informations de l'entreprise
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.black)
    p.drawString(40, height - 100, "KariPlus")
    p.drawString(40, height - 130, "Bamako, Mali")
    p.drawString(40, height - 145, "Téléphone: 00223 72 88 26 25")
    p.drawString(40, height - 160, "Email: kariplus@gmail.com")

    # Informations de la commande et de l'utilisateur
    p.drawString(40, height - 220, f"Client: {request.user.username}")
    p.drawString(40, height - 235, f"Commande #{commande.id}")
    if commande.date_commande:
        p.drawString(40, height - 250, f"Date: {commande.date_commande.strftime('%Y-%m-%d %H:%M:%S')}")

    # Tableau des articles commandés
    data = [["Produit", "Quantité", "Prix unitaire (FCFA)", "Total (FCFA)"]]
    for article in articles_commande:
        produit = article.produit
        quantite = article.quantité
        prix_unitaire = Decimal(produit.prix).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_article = (Decimal(produit.prix) * quantite).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        data.append([produit.nom, quantite, f"{prix_unitaire:.2f}", f"{total_article:.2f}"])

    table = Table(data, colWidths=[200, 100, 120, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#27ae60")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 40, height - 400)

    # Insérer le logo à droite et en dessous du cadre
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=4 * cm, height=4 * cm)
        logo.drawOn(p, width - 6 * cm, height - 240)

    # Pied de page avec le prix total et remerciements
    y = height - 420 - len(articles_commande) * 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, f"Prix total: {total_prix:.2f} FCFA")

    p.setLineWidth(1)
    p.line(40, y - 10, width - 40, y - 10)

    p.setFont("Helvetica", 10)
    p.drawString(40, y - 30, "Merci pour votre achat !")
    p.drawString(40, y - 50, "Pour toute question, contactez-nous à kariplus.com")

    # Sauvegarder et fermer le PDF
    p.showPage()
    p.save()

    return response


def contacts(request):
    # Logique de la vue
    context = {
        # Contexte si nécessaire
    }
    return render(request, 'contacts.html', context)
