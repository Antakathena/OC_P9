from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.urls import reverse
from PIL import Image
import logging

_logger = logging.getLogger(__name__)

class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True, default="L'avez-vous lu ?")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='cover_pics')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande à propos de \"{self.title}\" par {self.user}"

    def get_absolute_url(self):
        # return reverse('reviews-ticket-detail', kwargs={'pk': self.pk})
        # redirect renvoie à une adresse specifique
        # reverse va seulement donner l'adresse en string à la vue
        return reverse('reviews-myPosts')


    def save(self, *args, **kwargs):
        """
        surcharge la méthode existante pour retrecir les images trop grandes
        """
        try:
            super(Ticket,self).save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height > 200 or img.width > 200:
                output_size = (200,200)
                img.thumbnail(output_size)
                img.save(self.image.path)            
        except ValueError:
            _logger.debug("Pas d'image fournie")


class Review(models.Model):
    ticket = models.ForeignKey(related_name= "review",to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.headline}, commentaire par {self.user}"

    def get_absolute_url(self):
        # return reverse('reviews-review-detail', kwargs={'pk': self.pk})
        return reverse('reviews-myPosts')


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')
    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)

    def __str__(self):
        return f"{self.user} suit {self.followed_user}"


    def get_absolute_url(self):
        return reverse('reviews-myPosts')
    
