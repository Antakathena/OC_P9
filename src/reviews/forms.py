from django import forms
from django.utils.safestring import mark_safe
from django.db.models import Count

from django.contrib.auth.models import User
from .models import Ticket, Review, UserFollows


CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]
"""
Choices pour le radiobutton du ReviewForm.
Tuple key-value , key-Display value pairs (seen in the form).
"""

class HorizontalRadioRenderer(forms.RadioSelect):
    # tentative pour rendre les radio button à l'horizontale
    # mais quand on ajoute renderer= HorizontalRadioRenderer après choices dans le widget on a une erreur)
    # d'autres cadavres d'essais dans le CSS
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class TicketForm(forms.ModelForm):
    """
    Formulaire qui permet de créer un ticket pour demander une critique
    On peut ajouter une image qui sera redimensionnée par le modèle (facultative)
    """
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Veuillez indiquer le titre et l'auteur"
        self.fields['description'].label = "Formulez votre demande"  # ne pas afficher ce champ si review+ticket
        self.fields['image'].required = False
        
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        widgets = {
            'description': forms.Textarea(attrs={"class": "textarea", 'rows': '2'}),
        }


class ReviewForm(forms.ModelForm):
    """
    Formulaire qui permet de choisir le ticket existant auquel on veut répondre
    parmi ceux qui n'ont pas encore eu de réponse
    """
    def __init__(self, *args, ticket_id=None, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['ticket'].label = "Vous répondez à"
        # soit on a un ticket determiné soit on a une liste des tickets sans critique:
        ticket_id = ticket_id or self.fields['ticket'].initial or self.initial.get('ticket')
        if ticket_id:
            # là on a que le ticket voulu
            self.fields['ticket'].queryset = Ticket.objects.filter(id=ticket_id)
            self.fields['ticket'].initial = Ticket.objects.filter(id=ticket_id).all()
        else:
            # on a une liste des tickets qui n'ont pas encore de réponse
            self.fields['ticket'].queryset = Ticket.objects.annotate(nb_review=Count("review")).filter(nb_review=0)
        self.fields['rating'].label = "Donnez une note"
        self.fields['headline'].label = "Intitulé du commentaire"
        self.fields['body'].label = "Inscrivez votre commentaire"

    class Meta:
        model = Review
        fields = ('ticket', 'rating', 'headline', 'body')
        # on peut aussi écrire '__all__'
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'radio'}, choices=CHOICES),
            'body': forms.Textarea(attrs={"class": "textarea", 'rows': '10'})
        }


class TicketPlusReviewForm(forms.ModelForm):
    """
    Formulaire qui permet de créer le ticket
    quand on créé une critique
    et son ticket en même temps
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Veuillez indiquer le titre et l'auteur"
        self.fields['image'].required = False

    class Meta:
        model = Ticket
        fields = ('title', 'image')


class ReviewPlusTicketForm(forms.ModelForm):
    """
    Formulaire qui permet de créer une critique
    quand on créé une critique
    et son ticket en même temps
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = "Donnez une note"
        self.fields['headline'].label = "Intitulé du commentaire"
        self.fields['body'].label = "Inscrivez votre commentaire" 
           
 
    class Meta:
        model = Review
        fields = ('rating', 'headline', 'body')
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'radio'}, choices=CHOICES),
            'body': forms.Textarea(attrs={"class": "textarea", 'rows': '10'})
        }


class FollowForm(forms.ModelForm):
    def __init__(self, *args, username=None, following=None, followed_by=None,  **kwargs):
        """
        Username permet d'exclure de la liste des propositions l'utilisateur connecté.
        Following récupère ceux que l'on suit déjà. C'est une liste mais __in règler ce pb.
        """
        super(FollowForm, self).__init__(*args, **kwargs)
        self.username = username
        self.following = following
        self.followed_by = followed_by
        self.fields['followed_user'].label = "Choisir parmi :"
        self.fields['followed_user'].queryset = User.objects.all().exclude(
            username=self.username).exclude(id__in=[f.followed_user.id for f in self.following])

    class Meta:
        model = UserFollows
        fields = ('followed_user',)

        #  widgets = {
        #     'followed_user': forms.Textarea(attrs={"class":"textarea",'rows': '1'}),
        # }
        # si on voulait une zone de texte (mais après
        # il faut de toute façon vérifier qu'ils sont bien dans la db et pas suivis)
