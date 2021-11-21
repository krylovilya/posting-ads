from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'apps.main'
    default = True

    def ready(self):
        pass
