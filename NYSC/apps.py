from django.apps import AppConfig


class NyscConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NYSC'

    def ready(self):
        import NYSC.signals
