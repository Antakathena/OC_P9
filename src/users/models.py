from django.db import models
from django.contrib.auth.models import User
# PIL = pillow, the image library we added with pip install
# nb : d'autres packages font le resizing etc si projet + important
from PIL import Image
from itertools import chain

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def profiles_posts(self):
        # est-ce que ça fonctionne?
        reviews = self.review_set.all()
        tickets = self.ticket_set.all()
        posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
        )        
        return posts

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        override the existing method so we can add some parametres
        """
        super(Profile,self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
