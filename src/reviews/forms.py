from django import forms
from django.utils.safestring import mark_safe


from .models import Ticket, Review

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

# comment faire que le choix de la note dans review se fasse avec un radio button?
class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['ticket'].label = "Vous répondez à"
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

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        widgets = {
            'description': forms.Textarea(attrs={"class":"textarea",'rows': '2'})
        }

