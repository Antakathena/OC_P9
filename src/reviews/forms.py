from plistlib import UID
from django import forms
from django.utils.safestring import mark_safe
from django.db.models import Count

from django.contrib.auth.models import User
from .models import Ticket, Review, UserFollows
from users.models import Profile

# key-value , key-Display value pairs (seen in the form).
CHOICES=[
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5)
]

class HorizontalRadioRenderer(forms.RadioSelect):
    # tentative pour rendre les radio button à l'horizontale
    # mais quand on ajoute renderer= HorizontalRadioRenderer après choices dans le widget on a une erreur)
    # d'autres cadavres d'essais dans le CSS, mais la classe ne semble pas vouloir s'appliquer malgré le class ajouté aux attrs du widget
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['ticket'].label = "Vous répondez à"
        self.fields['ticket'].queryset = Ticket.objects.annotate(nb_review=Count("review")).filter(nb_review=0)
        self.fields['rating'].label = "Donnez une note"
        self.fields['headline'].label = "Intitulé du commentaire"
        self.fields['body'].label = "Inscrivez votre commentaire"

    class Meta:
        model = Review
        fields = ('ticket', 'rating', 'headline', 'body')
        widgets = {
            'rating':forms.RadioSelect(attrs={'class': 'radio'},choices=CHOICES),
            'body': forms.Textarea(attrs={"class":"textarea",'rows': '10'})
        }


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Veuillez indiquer le titre et l'auteur"
        self.fields['description'].label = "Formulez votre demande"
        self.fields['image'].required = False
        
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        widgets = {
            'description': forms.Textarea(attrs={"class":"textarea",'rows': '2'}),
        }

class FollowForm(forms.ModelForm):
    def __init__(self, *args, username=None, following=None, followed_by=None,  **kwargs):
        """ Username permet d'exclure de la liste des propositions l'utilisateur connecté
        mais following ne fonctionne pas pour exclure ceux qu'on suit déjà.
        C'est une liste mais __in devrait régler ce pb. Mais il y a user et followed_user à chaque fois"""
        super(FollowForm, self).__init__(*args, **kwargs)
        self.username = username
        self.following = following
        self.followed_by = followed_by
        self.fields['followed_user'].label = "Choisir parmi :"
        self.fields['followed_user'].queryset = User.objects.all().exclude(username=self.username).exclude(id__in=[f.followed_user.id for f in self.following])

        
    class Meta:
        model = UserFollows
        fields = ('followed_user',)
        # widgets = {
        #     'followed_user': forms.Textarea(attrs={"class":"textarea",'rows': '1'}),
        # }