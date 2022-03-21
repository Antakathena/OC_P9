from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

'''
# Dans la vidéo https://www.youtube.com/watch?v=1tZg5YLsCO4
# de Pyplane, voir sa vidéo pour signals pour comprendre à quoi/si ça sert

class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import profiles.signals

# ça va avec, dans init.py :
# default_app_config= 'profiles.apps.ProfilesConfig'
'''
