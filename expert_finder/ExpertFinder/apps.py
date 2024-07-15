from django.apps import AppConfig


class ExpertfinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ExpertFinder'

    def ready(self):
        import ExpertFinder.signals