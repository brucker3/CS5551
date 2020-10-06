from django.apps import AppConfig


class CheckersConfig(AppConfig):
    name = 'checkers'

    def ready(self):
        import checkers.signals
