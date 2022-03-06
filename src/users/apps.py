from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        # en lien avec signals.py, sert à créer automatiquement
        # le profil des nouveaux utilisateurs lorsqu'ils s'inscrivent
